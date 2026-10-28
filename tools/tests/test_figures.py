"""Body figures and marks, checked on the built site.

A screenshot, photograph, or drawing in a project's body copy is a `figure`
shortcode: a framed image with its size on the tag and a caption under it,
numbered by CSS so the markdown carries no numbers. A logo or wordmark is a
`mark`, unframed and uncaptioned. No project page carries a bare markdown
image any more. Builds the site into a scratch directory with zola; nothing
paid, nothing written into the tree.
"""
import pathlib
import re
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "content/projects"


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    if shutil.which("zola") is None:
        pytest.skip("zola is not installed")
    out = tmp_path_factory.mktemp("site")
    subprocess.run(["zola", "build", "-o", str(out), "-f"], cwd=ROOT, check=True, capture_output=True)
    return out


def page(site, slug):
    return (site / "projects" / slug / "index.html").read_text()


def figures(html):
    """Each figure's (src, alt, caption) in page order."""
    return re.findall(
        r"<figure class=figure><div class=figure__frame>"
        r"<img alt=(?:\"([^\"]*)\"|'([^']*)'|(\S+)) height=\d+ loading=lazy src=(\S+) width=\d+>"
        r"</div><figcaption>([^<]*)</figcaption></figure>",
        html,
    )


def test_no_project_page_carries_a_bare_markdown_image():
    for p in PROJECTS.glob("*.md"):
        body = p.read_text().split("+++", 2)[-1]
        assert not re.search(r"^!\[", body, re.M), p.name
        assert "<img" not in body, p.name


def test_a_figure_is_framed_sized_and_captioned(site):
    html = page(site, "cityhallmonitor")
    found = figures(html)
    assert len(found) == 1
    alt = next(a for a in found[0][:3] if a)
    src, caption = found[0][3], found[0][4]
    assert src == "/images/projects/cityhallmonitor.png"
    assert alt == "The City Hall Monitor search page"
    assert caption == alt, "the caption defaults to the alt text"


def test_figures_are_counted_by_css_not_by_the_markdown(site):
    html = page(site, "jacktaxa")
    assert len(figures(html)) == 2
    assert "Fig. 1" not in html and "FIG. 1" not in html
    assert 'counter-increment:fig' in (site / "style.css").read_text()


def test_a_mark_is_unframed_and_uncaptioned(site):
    html = page(site, "sensorgrid")
    assert re.search(r'<img alt=SensorGrid class=mark height=835 src=/images/projects/sensorgrid-logo.png width=759>', html)
    assert "<figcaption>SensorGrid<" not in html
    assert html.count("<figure class=figure>") == 2


def test_a_strip_mark_opens_jacktaxa_and_keeps_the_red_initial(site):
    html = page(site, "jacktaxa")
    assert 'class="mark mark--strip"' in html or "class=\"mark mark--strip\"" in html
    css = (site / "style.css").read_text()
    assert "p:first-of-type::first-letter" in css, "a mark above the first paragraph must not kill the initial"
