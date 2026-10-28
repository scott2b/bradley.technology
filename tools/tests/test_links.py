"""External links in body copy open off site, in a new tab; internal links do not.

Set by `external_links_target_blank` in config.toml, which also adds
rel=noopener. Builds the site into a scratch directory with zola.
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


def anchors(site, slug):
    html = (site / "projects" / slug / "index.html").read_text()
    return re.findall(r"<a [^>]*>", html)


def test_an_external_body_link_opens_in_a_new_tab(site):
    a = [t for t in anchors(site, "cityhallmonitor") if "documentcloud.org" in t]
    assert len(a) == 1
    assert "target=_blank" in a[0] and "rel=noopener" in a[0]


def test_an_internal_body_link_stays_in_the_tab(site):
    a = [t for t in anchors(site, "jacktaxa") if "/credentials/depaul-mscs/" in t]
    assert len(a) == 1
    assert "target=" not in a[0]


def test_grant_proposals_are_listed_thin_under_the_papers(site):
    """data/proposals.toml renders as a second, smaller list on the
    publications page: a heading, one item per proposal, no links into
    the site, and the papers still first."""
    import tomllib
    html = (site / "publications/index.html").read_text()
    proposals = tomllib.loads((ROOT / "data/proposals.toml").read_text())["proposal"]
    i = html.index("Grant proposals")
    assert html.index("Putting News in Context") < i, "papers come first"
    thin = html[i:]
    assert thin.count("<li class=pub>") == len(proposals)
    for g in proposals:
        assert g["title"] in thin
        assert g["program"] in thin
    assert "<h3 class=pub-title><a" not in thin, "a proposal has no page of its own"
