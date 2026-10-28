"""The experience page's chapters, from data/experience.toml and the
experience pages' front matter."""
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


def chapter(html, title):
    # the minifier may leave an ampersand bare or escape it
    m = re.search(r"<h3 class=xp-chapter>" + re.escape(title).replace(r"\&", "(?:&|&amp;)") + "<", html)
    assert m, f"no chapter titled {title!r}"
    rest = html[m.start():]
    j = rest.find("<h3 class=xp-chapter>", 1)
    return rest if j < 0 else rest[:j]


def test_the_teaching_chapter_dates_its_roles_and_lists_the_lab_mentoring(site):
    html = (site / "experience/index.html").read_text()
    ch = chapter(html, "Teaching & Mentoring")
    # a role the chapter asserts for a current engagement comes first
    assert re.search(r"Knight Lab</a>\s*<p class=xp-meta>Project advising · 2012–present<", ch)
    assert "2018–2024" in ch, "CU Boulder's end year"
    assert "2023–2025" in ch, "JournalismAI's dates"
    assert ch.index("Project advising") < ch.index("2018–2024") < ch.index("2023–2025")


def test_a_current_role_is_not_repeated_as_a_previous_one(site):
    html = (site / "experience/index.html").read_text()
    prev = html[html.index("Previous roles"):]
    assert "Senior engineer of software" not in prev
