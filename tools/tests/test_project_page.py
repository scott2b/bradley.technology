"""The drawn sheets, checked on the built site.

A project page carries a drafting title block under its plate (cells for
the title, the kinds of work, and who drew it), a facts rail that opens
with the plate number, and no fact in both places. The home page's Sheet 00
takes the same frame and names its number in the block, having no rail. An
experience page shares the project template and gets none of it. Builds the
site into a scratch directory with zola; nothing paid, nothing written into
the tree.
"""
import pathlib
import re
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    if shutil.which("zola") is None:
        pytest.skip("zola is not installed")
    out = tmp_path_factory.mktemp("site")
    subprocess.run(["zola", "build", "-o", str(out), "-f"], cwd=ROOT, check=True, capture_output=True)
    return out


def page(site, path):
    return (site / path / "index.html").read_text()


def band(html):
    """The title block's cells as {caption: entry}, or None when there is none."""
    # The last cell's closing tag is the first of the pair that ends the band.
    m = re.search(r'<div class=plate-band>(.*?</div>)</(?:div|figure)>', html, re.S)
    if not m:
        return None
    cells = re.findall(r'<span class=plate-band__label>([^<]*)</span>([^<]*)</div>', m.group(1))
    return dict(cells)


def rail_labels(html):
    m = re.search(r'<aside[^>]*class=facts>(.*?)</aside>', html)
    return re.findall(r"<dt>([^<]*)", m.group(1)) if m else None


def test_title_block_names_the_project_its_work_and_who_drew_it(site):
    b = band(page(site, "projects/newscompass"))
    assert b == {
        "Title": "News Compass",
        "Work": "Applications & data · Systems",
        "Drawn": "bradley.technology",
    }


def test_rail_opens_with_the_plate_number_and_repeats_nothing(site):
    html = page(site, "projects/newscompass")
    assert '<dd class=facts__plate>01<' in html
    labels = rail_labels(html)
    assert labels == ["Plate", "Year", "Where", "Setting"]
    assert "<dt>Year<dd>2026<" in html
    assert "<dt>Where<dd>Knight Lab<" in html


def test_every_project_with_a_plate_has_a_title_block(site):
    for p in (ROOT / "content/projects").glob("*.md"):
        if p.name == "_index.md":
            continue
        html = page(site, f"projects/{p.stem}")
        has_image = 'class="featured-image sheet"' in html
        assert (band(html) is not None) == has_image, p.name


def test_sheet_00_names_itself_in_the_block(site):
    html = (site / "index.html").read_text()
    assert 'class="hero-plate sheet"' in html
    assert band(html) == {
        "Title": "General arrangement",
        "Sheet": "00",
        "Drawn": "bradley.technology",
    }
    assert rail_labels(html) is None


def test_experience_pages_have_neither(site):
    html = page(site, "experience/avtec")
    assert band(html) is None
    assert rail_labels(html) is None


def img(html, src_part):
    """The img tag whose src contains src_part, or None."""
    m = re.search(r'<img [^>]*src=[^ >]*' + re.escape(src_part) + r'[^>]*>', html)
    return m.group(0) if m else None


def printless_plate_in(html):
    """The img tag of a project shown in this grid that is still on an older
    plate with no print, or None once every shown plate has been redrawn
    (the test then has nothing to pin)."""
    for md in sorted((ROOT / "content/projects").glob("*.md")):
        if md.name == "_index.md":
            continue
        front = md.read_text().split("+++")[1]
        if "\nprint = " in front:
            continue
        tag = img(html, f"/images/projects/{md.stem}.")
        if tag is not None:
            return tag
    return None


def test_a_drawn_sheet_carries_both_states_in_the_grid(site):
    html = page(site, "projects")
    tag = img(html, "newscompass")
    assert 'data-sheet=/images/projects/newscompass.webp' in tag
    assert 'data-print=/images/projects/newscompass-print.webp' in tag
    assert 'src=/images/projects/newscompass.webp' in tag       # the sheet without a script
    old = printless_plate_in(html)
    if old is not None:                                         # an older plate has no print
        assert 'data-print' not in old


def test_home_row_prints_its_third_plate_dark(site):
    html = (site / "index.html").read_text()
    tags = re.findall(r'<div class=proj-sel-img><img ([^>]*)>', html)
    assert len(tags) == 3
    assert 'src=/images/projects/newscompass.webp' in tags[0]
    assert 'src=/images/projects/overstory.webp' in tags[1]
    # The third slot asks for the print; it falls back to the plate while the
    # project has no sheet yet, and this pins which it is today.
    third = tags[2]
    assert ("-print.webp" in third) == ("data-print" in third)


def test_detail_page_always_shows_the_sheet(site):
    html = page(site, "projects/newscompass")
    assert 'class="featured-image sheet"' in html
    assert "newscompass-print.webp" not in html
