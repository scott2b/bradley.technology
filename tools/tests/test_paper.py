"""promote --paper: the sheet's tone is found and moved; nothing here touches the network."""
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import images  # noqa: E402


def drawn_sheet():
    """A tan sheet with dark ink lines and one red element, like a workshop plate."""
    im = Image.new("RGB", (400, 200), (223, 211, 188))
    d = ImageDraw.Draw(im)
    for x in range(20, 380, 15):
        d.line([(x, 20), (x + 8, 180)], fill=(63, 43, 28), width=2)
    d.ellipse([180, 80, 220, 120], outline=(167, 100, 77), width=3)
    return im


def test_paper_tone_is_the_sheet_not_the_ink():
    assert images.paper_tone(drawn_sheet()) == (223, 211, 188)


def test_paper_tone_is_found_on_a_warm_saturated_sheet():
    """A sheet drawn warmer than usual: every paper pixel's channels spread by
    50. A greyness test finds no paper on it and lands in the shadows."""
    warm = drawn_sheet()
    warm.paste((228, 210, 178), (0, 0) + warm.size)
    ImageDraw.Draw(warm).line([(20, 20), (380, 180)], fill=(46, 39, 30), width=3)
    assert images.paper_tone(warm) == (228, 210, 178)


def test_to_paper_moves_the_sheet_and_prints_the_ink_at_the_fixed_weight():
    out, tone = images.to_paper(drawn_sheet(), "#f0ede6")
    assert tone == (223, 211, 188)
    assert out.getpixel((5, 5)) == (240, 237, 230)
    assert out.getpixel((21, 22)) == images.INK_ON_PAPER


def test_two_sheets_drawn_at_different_pressures_print_at_one_weight():
    light, heavy = drawn_sheet(), drawn_sheet()
    for im, ink in ((light, (120, 100, 80)), (heavy, (30, 20, 12))):
        d = ImageDraw.Draw(im)
        for x in range(20, 380, 15):
            d.line([(x, 20), (x + 8, 180)], fill=ink, width=2)
    a, _ = images.to_paper(light)
    b, _ = images.to_paper(heavy)
    assert a.getpixel((21, 22)) == b.getpixel((21, 22)) == images.INK_ON_PAPER


def test_to_paper_leaves_a_white_sheet_alone():
    white = Image.new("RGB", (100, 50), (255, 255, 255))
    out, tone = images.to_paper(white, "#ffffff")
    assert tone == (255, 255, 255) and out.getpixel((1, 1)) == (255, 255, 255)


def test_no_paper_at_all_fails_loudly():
    import pytest
    red = Image.new("RGB", (100, 50), (200, 20, 20))
    with pytest.raises(SystemExit):
        images.paper_tone(red)


def test_negative_prints_paper_as_ink_and_ink_as_pale_line_and_keeps_red():
    out = images.negative(drawn_sheet())
    assert out.getpixel((5, 5)) == (28, 28, 28)             # paper -> site ink
    r, g, b = out.getpixel((21, 22))                         # ink -> pale line
    assert min(r, g, b) > 180, (r, g, b)
    assert out.getpixel((180, 100)) == (167, 100, 77)        # the red mark as drawn


def test_negative_of_a_blank_sheet_is_a_flat_ground():
    blank = Image.new("RGB", (100, 50), (240, 237, 230))
    assert images.negative(blank).getcolors() == [(5000, (28, 28, 28))]


def plate_tree(tmp_path, monkeypatch, slug="thing", candidate="workshop-1"):
    """A scratch tree with one candidate and one project page; promote writes there."""
    work, imgs, pages = tmp_path / "work", tmp_path / "imgs", tmp_path / "pages"
    (work / slug).mkdir(parents=True); imgs.mkdir(); pages.mkdir()
    drawn_sheet().resize((1200, 600)).save(work / slug / f"{candidate}.png")
    (pages / f"{slug}.md").write_text('+++\ntitle = "Thing"\n[extra]\nimage = "/old.webp"\nprint = "/old-print.webp"\n+++\nBody\n')
    monkeypatch.setattr(images, "ROOT", tmp_path)   # promote reports paths relative to it
    monkeypatch.setattr(images, "WORK", work)
    monkeypatch.setattr(images, "IMAGES", imgs)
    monkeypatch.setattr(images, "PROJECTS", pages)
    return imgs, pages / f"{slug}.md"


def args(**kw):
    from types import SimpleNamespace
    return SimpleNamespace(**{"quality": 82, "paper": None, **kw})


def test_promote_of_a_sheet_writes_the_print_beside_it_and_points_the_page_at_both(tmp_path, monkeypatch):
    imgs, page = plate_tree(tmp_path, monkeypatch)
    images.cmd_promote(args(slug="thing", candidate="workshop-1", paper="#f0ede6"))
    assert (imgs / "thing.webp").exists() and (imgs / "thing-print.webp").exists()
    fm = page.read_text()
    assert 'image = "/images/projects/thing.webp"\nprint = "/images/projects/thing-print.webp"\n' in fm
    assert fm.count("print =") == 1
    assert Image.open(imgs / "thing-print.webp").getpixel((5, 5)) == (28, 28, 28)
    assert fm.endswith("+++\nBody\n")


def test_promote_without_paper_has_no_print_and_drops_the_field(tmp_path, monkeypatch):
    imgs, page = plate_tree(tmp_path, monkeypatch)
    (imgs / "thing-print.webp").write_bytes(b"stale")
    images.cmd_promote(args(slug="thing", candidate="workshop-1"))
    assert (imgs / "thing.webp").exists() and not (imgs / "thing-print.webp").exists()
    fm = page.read_text()
    assert 'image = "/images/projects/thing.webp"\n' in fm and "print =" not in fm
