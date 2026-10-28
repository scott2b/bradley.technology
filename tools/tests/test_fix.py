"""fix: only the box changes, and the price check runs before any call.
The model call is replaced; nothing here touches the network."""
import io
import json
import pathlib
import sys
from types import SimpleNamespace

import pytest
from PIL import ImageStat, Image, ImageChops, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import images  # noqa: E402

MODEL = "test/model"
BOX = (100, 380, 160, 480)
BOX2 = (600, 100, 700, 200)


def sheet():
    im = Image.new("RGB", (1200, 600), (223, 211, 188))
    d = ImageDraw.Draw(im)
    for x in range(0, 1200, 15):
        d.line([(x, 0), (x + 8, 600)], fill=(63, 43, 28), width=2)
    return im


def tree(tmp_path, monkeypatch, price=0.14):
    work = tmp_path / "work"
    (work / "thing").mkdir(parents=True)
    sheet().save(work / "thing" / "workshop-1.png")
    if price is not None:
        (work / "log.jsonl").write_text(json.dumps({"model": MODEL, "images": 1, "cost": price}) + "\n")
    monkeypatch.setattr(images, "WORK", work)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test")
    monkeypatch.setattr(images, "load_env", lambda: None)
    calls = []

    def fake_call(model, prompt, refs=(), timeout=240):
        calls.append((model, prompt, refs))
        buf = io.BytesIO()
        Image.new("RGB", (1280, 720), (0, 0, 255)).save(buf, "PNG")   # the model's 16:9 frame
        return [buf.getvalue()], 0.14, ""
    monkeypatch.setattr(images, "call", fake_call)
    return work / "thing", calls


def args(**kw):
    return SimpleNamespace(**{"slug": "thing", "candidate": "workshop-1", "boxes": [list(BOX)],
                              "instruction": "remove the figure", "feather": 12,
                              "model": MODEL, "budget": 0.50, **kw})


def test_fix_changes_only_the_box_and_keeps_the_original(tmp_path, monkeypatch):
    out, calls = tree(tmp_path, monkeypatch)
    images.cmd_fix(args())
    assert len(calls) == 1 and "remove the figure" in calls[0][1]
    orig = Image.open(out / "workshop-1.png")
    fixed = Image.open(out / "workshop-1-fix-1.png")
    assert ImageChops.difference(orig, sheet()).getbbox() is None     # original untouched
    diff = ImageChops.difference(orig, fixed)
    x0, y0, x1, y1 = diff.getbbox()
    assert BOX[0] <= x0 and BOX[1] <= y0 and x1 <= BOX[2] and y1 <= BOX[3]
    assert fixed.getpixel((130, 430)) == (0, 0, 255)                   # centre fully replaced
    assert json.loads((out.parent / "log.jsonl").read_text().splitlines()[-1])["fix"] == "workshop-1"
    images.cmd_fix(args())
    assert (out / "workshop-1-fix-2.png").exists()                     # a second try is numbered


def changed_inside(before, after, boxes):
    """Every changed pixel lies in one of the boxes, and every box has a change."""
    diff = ImageChops.difference(before, after).convert("L")
    for x0, y0, x1, y1 in boxes:
        assert diff.crop((x0, y0, x1, y1)).getbbox() is not None
        ImageDraw.Draw(diff).rectangle([x0, y0, x1 - 1, y1 - 1], fill=0)
    return diff.getbbox() is None


def test_fix_takes_several_boxes_in_one_call(tmp_path, monkeypatch):
    out, calls = tree(tmp_path, monkeypatch)
    images.cmd_fix(args(boxes=[list(BOX), list(BOX2)]))
    assert len(calls) == 1
    assert changed_inside(sheet(), Image.open(out / "workshop-1-fix-1.png"), [BOX, BOX2])


def test_a_fix_of_a_fix_sends_the_mended_candidate_and_keeps_the_earlier_box(tmp_path, monkeypatch):
    out, calls = tree(tmp_path, monkeypatch)
    raw = Image.new("RGB", (1280, 720), (9, 9, 9))
    raw.save(out / "workshop-1.raw.png")
    images.cmd_fix(args())
    first = Image.open(out / "workshop-1-fix-1.png").copy()
    images.cmd_fix(args(candidate="workshop-1-fix-1", boxes=[list(BOX2)]))
    sent = Image.open(io.BytesIO(calls[-1][2][0])).convert("RGB")
    assert sent.size == (1280, 720)  # the raw drawing's frame
    # the first fix's blue box is in what the model saw, where crop() maps it
    centre = (BOX[0] + 20, BOX[1] + 20, BOX[2] - 20, BOX[3] - 20)        # inside the feather
    assert ImageStat.Stat(images.crop(sent).crop(centre)).mean[0] < 40  # blue, from the fix
    assert ImageStat.Stat(images.crop(sent).crop(BOX2)).mean[0] > 150   # still the sheet
    assert changed_inside(first, Image.open(out / "workshop-1-fix-1-fix-1.png"), [BOX2])


def test_uncrop_puts_a_candidate_back_where_crop_took_it():
    raw = Image.new("RGB", (1280, 720), (9, 9, 9))
    back = images.crop(images.uncrop(scribble(), raw))
    diff = ImageChops.difference(back, scribble()).convert("L")
    assert ImageStat.Stat(diff).mean[0] < 3
    shifted = images.crop(images.uncrop(scribble().transform((1200, 600), Image.Transform.AFFINE, (1, 0, 6, 0, 1, 0)), raw))
    assert ImageStat.Stat(ImageChops.difference(shifted, scribble()).convert("L")).mean[0] > 10


def test_fix_refuses_before_calling_when_over_budget_or_unpriced(tmp_path, monkeypatch):
    _, calls = tree(tmp_path, monkeypatch, price=0.90)
    with pytest.raises(SystemExit):
        images.cmd_fix(args())
    _, calls2 = tree(tmp_path / "b", monkeypatch, price=None)
    with pytest.raises(SystemExit):
        images.cmd_fix(args())
    assert calls == [] and calls2 == []


def test_mend_rejects_a_box_outside_the_image():
    with pytest.raises(ValueError):
        images.mend(sheet(), sheet(), [(1100, 500, 1300, 600)], 12)


def scribble(seed=3):
    """A drawing with no repeating pattern, so only one alignment fits."""
    import random
    rnd = random.Random(seed)
    im = Image.new("RGB", (1200, 600), (223, 211, 188))
    d = ImageDraw.Draw(im)
    for _ in range(400):
        x, y = rnd.randrange(1200), rnd.randrange(600)
        d.line([(x, y), (x + rnd.randrange(-60, 60), y + rnd.randrange(-60, 60))],
               fill=(63, 43, 28), width=2)
    return im


def test_align_undoes_a_redrawn_answers_shift_and_scale():
    orig = scribble()
    # the answer is the same drawing, 2% larger and moved, with the box repainted
    answer = orig.transform(orig.size, Image.Transform.AFFINE, (0.98, 0, 9, 0, 0.98, -6),
                            resample=Image.Resampling.BICUBIC, fillcolor=(223, 211, 188))
    ImageDraw.Draw(answer).rectangle([500, 250, 620, 350], fill=(0, 0, 255))
    box = (480, 230, 640, 370)
    moved, (sc, dx, dy, before, after) = images.align(orig, answer, [box])
    assert after < before / 3
    # round the box, where the feather blends, the moved answer matches the drawing
    ring = (box[0] - 40, box[1] - 40, box[2] + 40, box[3] + 40)
    diff = ImageChops.difference(orig.crop(ring), moved.crop(ring)).convert("L")
    ImageDraw.Draw(diff).rectangle([40, 40, 40 + box[2] - box[0], 40 + box[3] - box[1]], fill=0)
    from PIL import ImageStat
    assert ImageStat.Stat(diff).mean[0] < 4


def test_align_leaves_an_answer_that_already_fits():
    orig = scribble()
    moved, (sc, dx, dy, before, after) = images.align(orig, orig.copy(), [(480, 230, 640, 370)])
    assert (sc, dx, dy) == (1.0, 0, 0)
