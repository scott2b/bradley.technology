#!/usr/bin/env python3
"""Project imagery for bradley.technology.

Two kinds of image live under static/images/projects. Screenshots and photographs
are evidence and never go through a generative model; `frame` gives them one
consistent presentation. Marks stand in for work that has no picture worth showing;
`marks` pairs an art direction with a subject, both from data/marks.toml, asks an
image model to draw it, crops the result to 2:1 and leaves it in image-work/ for a
person to choose from. The direction is what makes the marks a set; a run over every
project under one direction is how the set gets made.

    python3 tools/images.py frame                # every shot in data/shots.toml
    python3 tools/images.py frame sensorgrid     # one of them
    python3 tools/images.py marks newscompass muster --style isometric --n 1
    python3 tools/images.py marks newscompass muster --all-styles --budget 2.00
    python3 tools/images.py marks socialcontext-open --style blueprint --alt lens --n 2
    python3 tools/images.py sheet newscompass muster
    python3 tools/images.py promote newscompass blueprint-1
    python3 tools/images.py promote newscompass workshop-4 --paper
    python3 tools/images.py check               # every project image is a plate
    python3 tools/images.py fix buzz workshop-cams-1 "remove the small standing figure" --box 78 365 146 485

Either way the result is the same object: a 1200x600 WebP at
static/images/projects/<slug>.webp, which `image` in the project's front matter
points at. Templates rely on that and draw one frame for everything.

A project may carry alternate subjects under [projects.<slug>.alt]; `--alt NAME`
draws that one instead and names the candidates <style>-<alt>-<n>, so a second
reading of a project sits beside the first without disturbing it.

A direction drawn on paper (workshop, codex) comes back on a tan sheet that reads
as parchment against the site's white ground. `promote --paper` finds the sheet's
own tone and its darkest ink and prints the drawing on PAPER, a light neutral just
off the page, at one fixed ink weight (INK_ON_PAPER), so every sheet in the set
carries the same colour of paper and the same weight of line whatever tan and
pressure the model drew it with. The candidate in image-work/ is left as drawn,
so the step is repeatable from it.

A candidate that is right except for one small thing (a stray figure, a garbled
part) is mended with `fix`: the drawing goes back to the same model with an
instruction, and only the boxes of the answer, given in the candidate's 1200x600
pixels with --box (repeatable) and feathered inside their edges, are laid onto the
candidate. Everything outside the boxes stays the original pixels; the command
checks that before saving. The model redraws rather than pastes, so its answer can
come back moved or scaled by a few per cent; before taking the boxes, the answer is
lined up with the candidate over the area round them (`align`), or every line at a
box edge doubles. The result is a new candidate, <candidate>-fix-<n>,
beside the one it mends, which is never overwritten; promote it like any other.
A fix can itself be mended; the model is always sent the first drawing's raw
frame, and only the new boxes are taken from its answer.

Marks and fix call OpenRouter (OPENROUTER_API_KEY in .env), one call per candidate
or edit. Marks stops when the running cost reported by the API reaches --budget;
fix refuses its one call when the model's last logged price is above --budget, or
when the model has no logged price at all. Every call is logged with its cost to
image-work/log.jsonl. Nothing else here touches the network.
"""
import argparse
import base64
import io
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "content" / "projects"
IMAGES = ROOT / "static" / "images" / "projects"
WORK = ROOT / "image-work"
BRIEFS = ROOT / "data" / "marks.toml"
SHOTS = ROOT / "data" / "shots.toml"
SRC = ROOT / "image-src" / "projects"
HAIRLINE = "#e5e5e5"

# The house system: plate size and the site's colours.
W, H = 1200, 600
BG, INK, MUTE, ACCENT = "#f8f9fa", "#333333", "#8d9199", "#e63946"
MUTE_OP = 0.55

DEFAULT_MODEL = "openai/gpt-5.4-image-2"
API = "https://openrouter.ai/api/v1/chat/completions"

PREAMBLE = """You are making a mark for a software engineer's portfolio site: one image
that stands beside a project's title. It must look professionally designed and belong
to a set drawn in the same direction. Draw exactly what the direction says, in the
manner it says.

Direction:
"""


# ------------------------------------------------------------------ helpers
def load_env():
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def briefs():
    import tomllib
    return tomllib.loads(BRIEFS.read_text())


def short(model):
    return model.split("/", 1)[1]


def data_url(png_bytes):
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode()


def palette_image():
    """The four house colours, with mute pre-blended onto the ground the way
    a hairline stroke at 0.55 opacity sits on the background)."""
    hx = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))
    bg, mute = hx(BG), hx(MUTE)
    blend = tuple(round(m * MUTE_OP + b * (1 - MUTE_OP)) for m, b in zip(mute, bg))
    cols = [bg, hx(INK), blend, hx(ACCENT)]
    pal = Image.new("P", (1, 1))
    flat = [c for col in cols for c in col]
    pal.putpalette(flat + flat[:3] * (256 - len(cols)))
    return pal


def crop(img):
    """Centre-crop to 2:1 and resize to 1200x600."""
    w, h = img.size
    if w / h > 2:
        nw = h * 2
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = w // 2
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)


def snap(img):
    """crop, then every pixel to the four house colours. Optional: it makes a
    flat drawing sit exactly on the site palette and destroys anything with
    shading, so it is off unless asked for."""
    q = crop(img).quantize(palette=palette_image(), dither=Image.Dither.NONE)
    return q.convert("RGB")


# ------------------------------------------------------------------ marks
def spent():
    log = WORK / "log.jsonl"
    if not log.exists():
        return 0.0
    return sum(json.loads(l).get("cost", 0) for l in log.read_text().splitlines() if l)


def call(model, prompt, refs=(), timeout=240):
    content = [{"type": "text", "text": prompt}]
    for r in refs:
        content.append({"type": "image_url", "image_url": {"url": data_url(r)}})
    body = {"model": model, "messages": [{"role": "user", "content": content}],
            "modalities": ["image", "text"], "image_config": {"aspect_ratio": "16:9"}}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={
        "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
        "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=timeout))
    msg = r["choices"][0]["message"]
    cost = (r.get("usage") or {}).get("cost", 0.0)
    images = []
    for im in msg.get("images") or []:
        m = re.match(r"data:([^;]+);base64,(.*)", im["image_url"]["url"])
        images.append(base64.b64decode(m.group(2)))
    return images, cost, (msg.get("content") or "")


def model_tag(model):
    """A short name for a model in candidate names: google/gemini-3-pro-image -> gemini."""
    return model.split("/")[-1].split("-")[0]


def cmd_marks(args):
    load_env()
    if "OPENROUTER_API_KEY" not in os.environ:
        sys.exit("OPENROUTER_API_KEY is not set")
    data = briefs()
    styles = list(data["styles"]) if args.all_styles else args.styles
    if not styles:
        sys.exit("give --style NAME (repeatable) or --all-styles; see data/marks.toml")
    for st in styles:
        if st not in data["styles"]:
            sys.exit(f"no style {st!r} in {BRIEFS.relative_to(ROOT)}")
    log = WORK / "log.jsonl"
    session = 0.0
    finish = snap if args.snap else crop
    for slug in args.slugs:
        subjects = {**data.get("site", {}), **data["projects"]}
        if slug not in subjects:
            sys.exit(f"{slug}: no subject in {BRIEFS.relative_to(ROOT)}")
        out = WORK / slug
        out.mkdir(parents=True, exist_ok=True)
        if args.alt:
            alts = subjects[slug].get("alt", {})
            if args.alt not in alts:
                sys.exit(f"{slug}: no alternate subject {args.alt!r} in {BRIEFS.relative_to(ROOT)}")
            subject = alts[args.alt]
        else:
            subject = subjects[slug]["subject"]
        for st in styles:
            stem = f"{st}-{args.alt}" if args.alt else st
            if args.model != DEFAULT_MODEL:   # another model's drawings sit beside, not over
                stem += "-" + model_tag(args.model)
            prompt = (PREAMBLE + data["styles"][st]["brief"].strip()
                      + "\n\nSubject:\n" + subject.strip())
            (out / f"{stem}.prompt.txt").write_text(prompt)
            for i in range(1, args.n + 1):
                if session >= args.budget:
                    print(f"budget of ${args.budget:.2f} reached (${session:.3f} spent); stopping")
                    return
                name = f"{stem}-{i}"
                if (out / f"{name}.png").exists() and not args.force:
                    print(f"{slug}/{name}: exists, skipping")
                    continue
                t = time.time()
                try:
                    images, cost, text = call(args.model, prompt)
                except urllib.error.HTTPError as e:
                    print(f"{slug}/{name}: HTTP {e.code} {e.read()[:400]!r}")
                    continue
                session += cost
                with log.open("a") as f:
                    f.write(json.dumps({"slug": slug, "style": st, "alt": args.alt,
                                        "model": args.model, "n": i,
                                        "cost": cost, "images": len(images),
                                        "seconds": round(time.time() - t, 1),
                                        "text": text[:200]}) + "\n")
                if not images:
                    print(f"{slug}/{name}: no image returned (${cost:.3f}) {text[:120]!r}")
                    continue
                raw = Image.open(io.BytesIO(images[0]))
                raw.save(out / f"{name}.raw.png")
                finish(raw).save(out / f"{name}.png")
                print(f"{slug}/{name}: {raw.size[0]}x{raw.size[1]} ${cost:.3f} "
                      f"{time.time() - t:.0f}s (session ${session:.2f})")
    print(f"session ${session:.2f}; all-time ${spent():.2f}")


# ------------------------------------------------------------------ fix
FIX_PROMPT = """This is a finished pen drawing on a paper sheet. Return the same drawing,
the same size and framing, line for line, with one change only:

{instruction}

Where something is removed, continue the lines, paper and shading behind it so the
place reads as if it had never been there. Change nothing else."""


def last_price(model):
    """The cost of the most recent logged call to `model` that returned an image,
    or None when there is none."""
    log = WORK / "log.jsonl"
    if not log.exists():
        return None
    rows = [json.loads(l) for l in log.read_text().splitlines() if l]
    rows = [r for r in rows if r.get("model") == model and r.get("images") and r.get("cost")]
    return rows[-1]["cost"] if rows else None


def mend(orig, edited, boxes, feather):
    """Lay the boxes of `edited` onto `orig`. Each box's mask is solid inside the
    box less `feather` and fades to nothing at the box edge, so no pixel outside
    the boxes changes. Both images are the same size."""
    orig, edited = orig.convert("RGB"), edited.convert("RGB")
    mask = Image.new("L", orig.size, 0)
    inside = Image.new("L", orig.size, 0)
    for box in boxes:
        x0, y0, x1, y1 = box
        if not (0 <= x0 < x1 <= orig.width and 0 <= y0 < y1 <= orig.height):
            raise ValueError(f"box {box} is not inside {orig.size}")
        f = max(0, min(feather, (x1 - x0) // 4, (y1 - y0) // 4))
        one = Image.new("L", orig.size, 0)
        ImageDraw.Draw(one).rectangle([x0 + f, y0 + f, x1 - 1 - f, y1 - 1 - f], fill=255)
        if f:
            one = one.filter(ImageFilter.GaussianBlur(f / 2))
        hard = Image.new("L", orig.size, 0)    # clip the blur's tail to the box
        ImageDraw.Draw(hard).rectangle([x0, y0, x1 - 1, y1 - 1], fill=255)
        mask = ImageChops.lighter(mask, ImageChops.multiply(one, hard))
        inside = ImageChops.lighter(inside, hard)
    out = Image.composite(edited, orig, mask)
    outside = ImageChops.multiply(ImageChops.difference(out, orig).convert("L"),
                                  ImageChops.invert(inside))
    if outside.getbbox() is not None:
        raise AssertionError("pixels changed outside the boxes")
    return out


def align(orig, edited, boxes, pad=80):
    """Line `edited` up with `orig` around the boxes. An image model's answer is
    redrawn, not pasted: the whole drawing can come back moved and scaled by a
    few per cent, and a box taken from it unaligned doubles every line at its
    edge. This searches scale and shift, first at quarter size and then at full
    size, for the best match over the area round the boxes, leaving the boxes
    out since they are meant to differ. Returns the moved image and (scale, dx,
    dy, mismatch before, mismatch after); the mismatch is mean grey difference."""
    x0 = max(0, min(b[0] for b in boxes) - pad); y0 = max(0, min(b[1] for b in boxes) - pad)
    x1 = min(orig.width, max(b[2] for b in boxes) + pad); y1 = min(orig.height, max(b[3] for b in boxes) + pad)
    ref, mov = orig.convert("L"), edited.convert("L")
    keep = Image.new("L", orig.size, 255)
    for b in boxes:
        ImageDraw.Draw(keep).rectangle([b[0], b[1], b[2] - 1, b[3] - 1], fill=0)

    def scorer(k):
        size = (max(1, (x1 - x0) // k), max(1, (y1 - y0) // k))
        r = ref.resize((ref.width // k, ref.height // k), Image.Resampling.BOX).crop(
            (x0 // k, y0 // k, x0 // k + size[0], y0 // k + size[1]))
        m = mov.resize((mov.width // k, mov.height // k), Image.Resampling.BOX)
        w = keep.resize((keep.width // k, keep.height // k)).crop(
            (x0 // k, y0 // k, x0 // k + size[0], y0 // k + size[1]))
        n = max(1, ImageStat.Stat(w).sum[0] / 255)

        def score(sc, dx, dy):
            t = m.transform(size, Image.Transform.AFFINE,
                            (sc, 0, sc * (x0 // k) + dx / k, 0, sc, sc * (y0 // k) + dy / k),
                            resample=Image.Resampling.BILINEAR, fillcolor=255)
            return ImageStat.Stat(ImageChops.multiply(ImageChops.difference(r, t), w)).sum[0] / 255 / n
        return score

    coarse, fine = scorer(4), scorer(1)
    before = fine(1.0, 0, 0)
    best = min(((coarse(sc / 1000, dx, dy), sc / 1000, dx, dy)
                for sc in range(940, 1061, 5) for dx in range(-48, 49, 4) for dy in range(-48, 49, 4)))
    _, bs, bx, by = best
    best = min(((fine(bs + ds / 1000, bx + dx, by + dy), bs + ds / 1000, bx + dx, by + dy)
                for ds in range(-5, 6) for dx in range(-4, 5) for dy in range(-4, 5)))
    after, sc, dx, dy = best
    if after >= before:
        return edited.convert("RGB"), (1.0, 0, 0, before, before)
    moved = edited.convert("RGB").transform(orig.size, Image.Transform.AFFINE,
                                            (sc, 0, dx, 0, sc, dy),
                                            resample=Image.Resampling.BICUBIC, fillcolor=(255, 255, 255))
    return moved, (sc, dx, dy, before, after)


def root_raw(out, candidate):
    """The raw frame a candidate was cropped from; a fix of a fix shares the first
    drawing's."""
    return out / (re.sub(r"(-fix-\d+)+$", "", candidate) + ".raw.png")


def uncrop(img, raw):
    """img laid back into the raw frame where crop() took it from, so the model sees
    the candidate as it now stands, earlier fixes included, in its own geometry."""
    w, h = raw.size
    if w / h > 2:
        nw = h * 2
        rect = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = w // 2
        rect = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    out = raw.convert("RGB")
    out.paste(img.convert("RGB").resize((rect[2] - rect[0], rect[3] - rect[1]),
                                        Image.Resampling.LANCZOS), rect[:2])
    return out


def cmd_fix(args):
    load_env()
    if "OPENROUTER_API_KEY" not in os.environ:
        sys.exit("OPENROUTER_API_KEY is not set")
    out = WORK / args.slug
    src = out / f"{args.candidate}.png"
    if not src.exists():
        sys.exit(f"no candidate {src}")
    price = last_price(args.model)
    if price is None:
        sys.exit(f"{args.model} has no logged price; draw one mark with it first")
    if price > args.budget:
        sys.exit(f"{args.model} last cost ${price:.3f}, above the budget of ${args.budget:.2f}")
    # The candidate goes back in the raw drawing's 16:9 frame, so the answer comes
    # in the same geometry and crop() maps it onto the candidate as it did the first
    # time. A fix of a fix sends the candidate as mended, not the first drawing,
    # or the model would see, and redraw, what earlier fixes took out. A candidate
    # without a raw frame is sent as it is.
    raw = root_raw(out, args.candidate)
    if raw.exists():
        buf = io.BytesIO()
        uncrop(Image.open(src), Image.open(raw)).save(buf, "PNG")
        ref = buf.getvalue()
    else:
        ref = src.read_bytes()
    prompt = FIX_PROMPT.format(instruction=args.instruction.strip())
    n = 1
    while (out / f"{args.candidate}-fix-{n}.png").exists():
        n += 1
    name = f"{args.candidate}-fix-{n}"
    t = time.time()
    images, cost, text = call(args.model, prompt, refs=[ref])
    with (WORK / "log.jsonl").open("a") as f:
        f.write(json.dumps({"slug": args.slug, "fix": args.candidate, "boxes": args.boxes,
                            "model": args.model, "n": n, "cost": cost,
                            "images": len(images), "seconds": round(time.time() - t, 1),
                            "text": text[:200]}) + "\n")
    if not images:
        sys.exit(f"{args.slug}/{name}: no image returned (${cost:.3f}) {text[:120]!r}")
    edited = Image.open(io.BytesIO(images[0]))
    edited.save(out / f"{name}.edit.png")
    orig, boxes = Image.open(src).convert("RGB"), [tuple(b) for b in args.boxes]
    moved, (sc, dx, dy, before, after) = align(orig, crop(edited), boxes)
    print(f"aligned: scale {sc:.3f}, shift {dx:+d},{dy:+d}; mismatch round the boxes {before:.3f} -> {after:.3f}")
    fixed = mend(orig, moved, boxes, args.feather)
    fixed.save(out / f"{name}.png")
    (out / f"{name}.prompt.txt").write_text(prompt)
    print(f"{args.slug}/{name}: boxes {args.boxes}, edit {edited.size[0]}x{edited.size[1]}, "
          f"${cost:.3f} {time.time() - t:.0f}s; all-time ${spent():.2f}")


# ------------------------------------------------------------------ sheet
def cmd_sheet(args):
    """One contact sheet per slug: the current mark, then every candidate."""
    from PIL import ImageDraw
    cw, ch, pad, cols = 560, 280, 14, 2
    for slug in args.slugs:
        d = WORK / slug
        cells = []
        for cur in (IMAGES / f"{slug}.webp", ROOT / "static" / "images" / f"{slug}.webp"):
            if cur.exists():
                cells.append(("current", Image.open(cur).convert("RGB")))
                break
        for c in sorted(p for p in d.glob("*.png")
                        if not p.name.endswith(".raw.png") and p.name != "sheet.png"):
            cells.append((c.stem, Image.open(c).convert("RGB")))
        rows = -(-len(cells) // cols)
        sheet = Image.new("RGB", (pad + cols * (cw + pad), pad + rows * (ch + 24 + pad)), "white")
        dr = ImageDraw.Draw(sheet)
        for k, (label, im) in enumerate(cells):
            x = pad + (k % cols) * (cw + pad)
            y = pad + (k // cols) * (ch + 24 + pad)
            dr.text((x, y), f"{slug}: {label}", fill="black")
            sheet.paste(im.resize((cw, ch)), (x, y + 20))
        outp = d / "sheet.png"
        sheet.save(outp)
        print(outp)


# ------------------------------------------------------------------ promote
def point_page(slug, print_too):
    """Set the project's front-matter `image` to its plate and `print` to its
    negative, or drop `print` when the plate has none."""
    page = PROJECTS / f"{slug}.md"
    text = page.read_text()
    head, fm, body = text.split("+++", 2)
    fm = re.sub(r'^print = ".*"\n', "", fm, flags=re.M)
    line = f'image = "/images/projects/{slug}.webp"'
    if print_too:
        line += f'\nprint = "/images/projects/{slug}-print.webp"'
    fm, n = re.subn(r'^image = ".*"$', line, fm, flags=re.M)
    if n != 1:
        sys.exit(f"{page.name}: expected one image line in front matter, found {n}")
    page.write_text(head + "+++" + fm + "+++" + body)


def save_plate(img, dst, quality):
    if img.size != (W, H):
        sys.exit(f"{dst.name}: plate is {img.size}, not {W}x{H}")
    img.convert("RGB").save(dst, quality=quality, method=6)


PAPER = "#f0ede6"
INK_ON_PAPER = (67, 59, 48)   # the sepia the first liked sheet printed at


def _hex(c):
    return tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def _small(img):
    """A 300px-wide box-filtered copy: nothing rings brighter than the sheet."""
    return img.convert("RGB").resize((300, round(300 * img.height / img.width)), Image.BOX)


def _lum(q):
    return round(0.299 * q[0] + 0.587 * q[1] + 0.114 * q[2])


def _pixels(img):
    """Every pixel, flat; get_flattened_data where Pillow has it (11+)."""
    return list(img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata())


def sheet_luminance(lum_values):
    """The sheet's luminance: the 70th percentile. Open paper is most of a
    drawn sheet, so this lands on the paper and not on a line."""
    ordered = sorted(lum_values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * 0.7))]


def paper_tone(img):
    """The sheet's colour: the per-channel median of the pixels at the sheet's
    luminance, red excluded.

    Found by luminance and not by greyness: parchment is a tan, and a sheet
    drawn a little warmer than usual has every pixel more saturated than any
    grey threshold, which once sent the finder to the shadows instead."""
    px = _pixels(_small(img))
    lum = [_lum(q) for q in px]
    sheet = sheet_luminance(lum)
    near = [q for q, l in zip(px, lum) if abs(l - sheet) <= 12 and q[0] - max(q[1], q[2]) < 50]
    if not near:
        sys.exit("no paper found: nothing at the sheet's luminance but red")
    mid = len(near) // 2
    return tuple(sorted(q[i] for q in near)[mid] for i in range(3))


def ink_tone(img, tone):
    """The drawing's darkest ink: the mean colour of the darkest hundredth of
    the sheet's pixels, or None when nothing on it is much darker than the
    paper. Measured at full size: a pen line is a pixel or two wide, and any
    filtered copy mixes it with the paper and reads it lighter than it is."""
    rgb = img.convert("RGB")
    hist = rgb.convert("L").histogram()
    total, acc, cut = sum(hist), 0, 0
    for v, c in enumerate(hist):
        acc += c
        if acc >= total / 100:
            cut = v
            break
    mask = rgb.convert("L").point(lambda v, cut=cut: 255 if v <= cut else 0)
    stat = ImageStat.Stat(rgb, mask)
    ink = tuple(round(m) for m in stat.mean)
    if _lum(tone) - _lum(ink) < 60:
        return None
    return ink


def to_paper(img, target=PAPER):
    """Print the sheet on `target` paper at the fixed ink weight.

    Per channel, an affine map through two anchors: the sheet's tone goes to
    the target and its darkest ink goes to INK_ON_PAPER, so the open paper,
    the faint construction lines, and the full pen strokes all land where
    every other sheet's do. The red rides the same map and comes out the
    muted accent the brief asks for. A sheet with no ink on it is only
    scaled, tone to target. Clipped at black and white."""
    t = _hex(target)
    tone = paper_tone(img)
    ink = ink_tone(img, tone)
    bands = img.convert("RGB").split()
    out = []
    for band, pc, tc, ic in zip(bands, tone, t, INK_ON_PAPER):
        if ink is None:
            g = tc / max(1, pc)
            out.append(band.point(lambda v, g=g: min(255, round(v * g))))
        else:
            kc = ink[len(out)]
            slope = (tc - ic) / max(1, pc - kc)
            out.append(band.point(lambda v, s=slope, pc=pc, tc=tc: max(0, min(255, round(tc + (v - pc) * s)))))
    return Image.merge("RGB", out), tone


INK = "#1c1c1c"
LINE = "#e6e3dc"


def negative(img, ink=INK, line=LINE):
    """The same drawing printed as a negative: the paper becomes the site's ink
    and the ink becomes a paper-pale line, so a sheet and its print are one
    drawing in two states and a layout can set them against each other.

    Line strength is how far a pixel sits below the sheet's luminance (see
    sheet_luminance), full at 40; the 0.8 power keeps faint
    construction lines visible. The red mark is kept as drawn."""
    rgb = img.convert("RGB")
    lum = rgb.convert("L")
    paper = sheet_luminance(_pixels(lum))
    ink_c, line_c = _hex(ink), _hex(line)
    span = max(1, paper - 40)

    def strength(v):
        return min(1.0, max(0.0, (paper - v) / span)) ** 0.8

    out = Image.merge("RGB", [
        lum.point(lambda v, a=a, b=b: round(a + (b - a) * strength(v)))
        for a, b in zip(ink_c, line_c)
    ])
    r, g, b = rgb.split()
    red = ImageChops.multiply(
        r.point(lambda v: 255 if v > 120 else 0),
        ImageChops.multiply(
            ImageChops.subtract(r, g.point(lambda v: min(255, int(v * 1.6)))).point(lambda v: 255 if v else 0),
            ImageChops.subtract(r, b.point(lambda v: min(255, int(v * 1.6)))).point(lambda v: 255 if v else 0),
        ),
    )
    return Image.composite(rgb, out, red)


def cmd_promote(args):
    """Copy a chosen candidate into static/ as WebP and point the project at it.

    A drawn sheet (promoted with --paper) also gets its negative print beside it,
    <slug>-print.webp, and the page's `print` field; a plate that is not a sheet
    has no print and the field is dropped. A site-level plate (a [site.*] subject
    in data/marks.toml) has no project page; it goes to static/images/<slug>.webp
    and a template refers to it directly."""
    src = WORK / args.slug / f"{args.candidate}.png"
    if not src.exists():
        sys.exit(f"no candidate {src}")
    img = Image.open(src)
    note = ""
    if args.paper:
        img, tone = to_paper(img, args.paper)
        note = ", paper #%02x%02x%02x -> %s" % (*tone, args.paper)
    if args.slug in briefs().get("site", {}):
        dst = ROOT / "static" / "images" / f"{args.slug}.webp"
        save_plate(img, dst, args.quality)
        print(f"{dst.relative_to(ROOT)} ({dst.stat().st_size // 1024} KB) <- {src.relative_to(ROOT)}{note}")
        return
    dst = IMAGES / f"{args.slug}.webp"
    save_plate(img, dst, args.quality)
    neg = IMAGES / f"{args.slug}-print.webp"
    if args.paper:
        save_plate(negative(img), neg, args.quality)
        note += f"; {neg.name} ({neg.stat().st_size // 1024} KB)"
    elif neg.exists():
        neg.unlink()
        note += f"; {neg.name} removed"
    point_page(args.slug, bool(args.paper))
    print(f"{dst.relative_to(ROOT)} ({dst.stat().st_size // 1024} KB) <- {src.relative_to(ROOT)}{note}; {args.slug}.md updated")


# ------------------------------------------------------------------ frame
def plate(img, fit, anchor=0.0):
    """One 1200x600 plate from a screenshot or photograph.

    crop: scale to fill the plate and take the 2:1 window `anchor` of the way
    down the source (0 top, 1 bottom). matte: the image at its own size on the
    off-white ground, never enlarged, scaled down only if it would touch the
    edges, with a hairline round it so it reads as an object."""
    img = img.convert("RGB")
    w, h = img.size
    if fit == "crop":
        scale = max(W / w, H / h)
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        w, h = img.size
        x = (w - W) // 2
        y = round((h - H) * anchor)
        return img.crop((x, y, x + W, y + H))
    if fit == "matte":
        scale = min(1.0, 0.8 * W / w, 0.8 * H / h)
        if scale < 1.0:
            img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
            w, h = img.size
        out = Image.new("RGB", (W, H), BG)
        x, y = (W - w) // 2, (H - h) // 2
        from PIL import ImageDraw
        ImageDraw.Draw(out).rectangle((x - 1, y - 1, x + w, y + h), outline=HAIRLINE)
        out.paste(img, (x, y))
        return out
    sys.exit(f"unknown fit {fit!r}")


def shots():
    import tomllib
    with open(SHOTS, "rb") as f:
        return tomllib.load(f)


def cmd_frame(args):
    """Make the plate for every shot in data/shots.toml, or the slugs given."""
    data = shots()
    slugs = args.slugs or sorted(data)
    for slug in slugs:
        if slug not in data:
            sys.exit(f"{slug} is not in {SHOTS.relative_to(ROOT)}")
        spec = data[slug]
        src = SRC / spec["src"]
        if not src.exists():
            sys.exit(f"missing original {src.relative_to(ROOT)}")
        dst = IMAGES / f"{slug}.webp"
        save_plate(plate(Image.open(src), spec["fit"], spec.get("anchor", 0.0)), dst, args.quality)
        point_page(slug)
        print(f"{dst.relative_to(ROOT)} ({dst.stat().st_size // 1024} KB) <- {spec['src']} {spec['fit']}")


def cmd_check(args):
    """Every project points at a plate that exists and is 1200x600. Exit 1 if not."""
    bad = 0
    for page in sorted(PROJECTS.glob("*.md")):
        if page.name == "_index.md":
            continue
        m = re.search(r'^image = "(.*)"$', page.read_text(), re.M)
        if not m:
            print(f"{page.name}: no image"); bad += 1; continue
        f = ROOT / "static" / m.group(1).lstrip("/")
        if not f.exists():
            print(f"{page.name}: {m.group(1)} missing"); bad += 1; continue
        size = Image.open(f).size
        if size != (W, H):
            print(f"{page.name}: {m.group(1)} is {size[0]}x{size[1]}"); bad += 1
    print(f"{bad} problem(s)" if bad else "every project image is a plate")
    sys.exit(1 if bad else 0)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("marks", help="ask an image model for mark candidates")
    m.add_argument("slugs", nargs="+")
    m.add_argument("--style", dest="styles", action="append", default=[], help="direction from data/marks.toml; repeatable")
    m.add_argument("--all-styles", action="store_true", help="every direction in data/marks.toml")
    m.add_argument("--alt", help="an alternate subject from [projects.<slug>.alt]")
    m.add_argument("--model", default=DEFAULT_MODEL)
    m.add_argument("--n", type=int, default=1, help="candidates per direction")
    m.add_argument("--snap", action="store_true", help="snap output to the four house colours")
    m.add_argument("--budget", type=float, default=2.0, help="stop when this session's cost reaches this, USD")
    m.add_argument("--force", action="store_true", help="regenerate candidates that already exist")
    m.set_defaults(fn=cmd_marks)
    s = sub.add_parser("sheet", help="contact sheet of candidates")
    s.add_argument("slugs", nargs="+")
    s.set_defaults(fn=cmd_sheet)
    p = sub.add_parser("promote", help="copy a chosen candidate into static/")
    p.add_argument("slug"); p.add_argument("candidate")
    p.add_argument("--quality", type=int, default=82)
    p.add_argument("--paper", nargs="?", const=PAPER, default=None, metavar="HEX",
                   help=f"bring the drawn sheet's tone to this colour (default {PAPER})")
    p.set_defaults(fn=cmd_promote)
    f = sub.add_parser("frame", help="plates from the screenshots and photographs in data/shots.toml")
    f.add_argument("slugs", nargs="*")
    f.add_argument("--quality", type=int, default=82)
    f.set_defaults(fn=cmd_frame)
    x = sub.add_parser("fix", help="mend one box of a candidate with an image edit")
    x.add_argument("slug"); x.add_argument("candidate")
    x.add_argument("instruction", help="what to change inside the boxes")
    x.add_argument("--box", dest="boxes", action="append", nargs=4, type=int, required=True,
                   metavar=("X0", "Y0", "X1", "Y1"),
                   help="a region to replace, in the candidate's 1200x600 pixels; repeatable")
    x.add_argument("--feather", type=int, default=12, help="fade width inside the box edge, px")
    x.add_argument("--model", default=DEFAULT_MODEL)
    x.add_argument("--budget", type=float, default=0.50, help="refuse the call if the model's last price is above this, USD")
    x.set_defaults(fn=cmd_fix)
    c = sub.add_parser("check", help="every project image exists and is a plate")
    c.set_defaults(fn=cmd_check)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
