"""Team lists on experience pages, from data/teams.toml.

An experience page that sets `team` in its front matter renders a People
section: the people Scott worked with there, each either a person link (an
id in people.toml, with the hover card) or a plain name. A project page can
then point at the list instead of naming a team from memory.
"""
import pathlib
import re
import shutil
import subprocess
import tomllib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    if shutil.which("zola") is None:
        pytest.skip("zola is not installed")
    out = tmp_path_factory.mktemp("site")
    subprocess.run(["zola", "build", "-o", str(out), "-f"], cwd=ROOT, check=True, capture_output=True)
    return out


def test_every_team_member_is_a_person_id_or_a_plain_name():
    people = tomllib.loads((ROOT / "data/people.toml").read_text())
    teams = tomllib.loads((ROOT / "data/teams.toml").read_text())
    for key, team in teams.items():
        for m in team["members"]:
            looks_like_id = re.fullmatch(r"[a-z0-9-]+", m) is not None
            if looks_like_id:
                assert m in people, f"{key}: {m} is not in people.toml"
            else:
                assert " " in m, f"{key}: {m} is neither an id nor a full name"


def test_the_infolab_page_renders_its_list(site):
    html = (site / "experience/infolab/index.html").read_text()
    m = re.search(r"<section [^>]*id=people[^>]*>", html)
    assert m, "the People section is missing or has no id to link to"
    people = html[m.end():]
    people = people[:people.index("</section>")]
    assert "<h3>" not in people, "one flat list, no groups"
    assert "People I worked with at the InfoLab" in people, "the heading says whose list this is"
    assert re.search(r"class=person href=\S+[^>]*>Larry Birnbaum<", people)
    members = tomllib.loads((ROOT / "data/teams.toml").read_text())["infolab"]["members"]
    ids = [m for m in members if re.fullmatch(r"[a-z0-9-]+", m)]
    assert people.count("<li>") == len(members), "one item per member, linked or plain"
    anchors = re.findall(r"<a [^>]*\bclass=person[\s>]", people)
    assert len(anchors) == len(ids), "a link for each member with a profile, and only those"


def test_a_page_without_a_team_has_no_list(site):
    html = (site / "experience/nortel/index.html").read_text()
    assert "id=people" not in html


def test_listening_post_points_at_the_infolab_list(site):
    html = (site / "projects/listening-post/index.html").read_text()
    assert 'href=/experience/infolab/#people' in html
