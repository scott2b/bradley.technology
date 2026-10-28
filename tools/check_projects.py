#!/usr/bin/env python3
"""Drive every filter on /projects/ in a real browser and check what is on screen.

The projects page is two tiers filtered in place by inline JS: a grid with
imagery and an index. Nothing about the filtering is visible in the source --
the first version of this design shipped with the tier counts going stale, and
it looked fine in the HTML. So this loads the built page, clicks each filter,
and reports what is actually visible.

Usage:  python3 tools/check_projects.py [--url http://127.0.0.1:1111/projects/]

Needs a running `zola serve` (default port 1111) and Google Chrome. Exits
non-zero on the first failed check.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PROBE = """
<script>
(function () {
  function state() {
    function vis(sel) {
      return Array.prototype.slice.call(document.querySelectorAll(sel))
        .filter(function (el) { return !el.hidden; });
    }
    return {
      sels: vis('#proj-sels > *').map(function (el) {
        return el.querySelector('.proj-sel-title').textContent.trim();
      }),
      rows: vis('#proj-rows > *').map(function (el) {
        return el.querySelector('.proj-row-title').textContent.trim();
      }),
      labels: Array.prototype.slice.call(document.querySelectorAll('.rule-label'))
        .map(function (el) {
          return {id: el.id, hidden: !!el.hidden,
                  count: el.querySelector('b').textContent.trim()};
        }),
      empty: !document.querySelector('.filter-empty').hidden,
      pressed: Array.prototype.slice.call(document.querySelectorAll('.filter'))
        .filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; })
        .map(function (b) { return b.dataset.filter; })
    };
  }

  var out = {buttons: [], states: {}, initial: state()};
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.filter'));
  buttons.forEach(function (b) {
    out.buttons.push({
      name: b.dataset.filter,
      label: b.childNodes[0].textContent.trim(),
      count: parseInt(b.querySelector('.filter-count').textContent.trim(), 10)
    });
  });
  buttons.forEach(function (b) { b.click(); out.states[b.dataset.filter] = state(); });
  // Back to All last, so the reported end state is the one a visitor lands on.
  buttons[0].click();
  out.states['all-again'] = state();
  console.log('PROBE ' + JSON.stringify(out));
})();
</script>
"""


def collect(url, frag=""):
    """Load the page with a probe appended and return what the probe saw.

    `frag` is a URL fragment to land on, which is how the homepage links in --
    each capability on the front page opens this page with its filter applied.
    """
    html = urllib.request.urlopen(url).read().decode()
    base = url.rsplit("/projects/", 1)[0] + "/"
    html = html.replace("<head>", f'<head><base href="{base}">', 1)
    if "</body>" in html:
        html = html.replace("</body>", PROBE + "</body>", 1)
    else:
        html += PROBE

    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "probe.html"
        page.write_text(html)
        proc = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=6000", "--enable-logging=stderr", "--v=0",
             "--dump-dom", page.as_uri() + frag],
            capture_output=True, text=True, timeout=90)

    hit = re.search(r'PROBE (\{.*\})', proc.stderr)
    if not hit:
        sys.exit("probe produced no output; is Chrome at %s?\n%s"
                 % (CHROME, proc.stderr[-2000:]))
    return json.loads(hit.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:1111/projects/")
    args = ap.parse_args()

    data = collect(args.url)
    buttons = data["buttons"]
    states = data["states"]
    fails = []

    def check(ok, msg):
        print(("  ok   " if ok else "  FAIL ") + msg)
        if not ok:
            fails.append(msg)

    total = buttons[0]["count"]
    print(f"\n{len(buttons)} filters, {total} projects\n")

    print("all")
    a = states["all"]
    check(len(a["sels"]) + len(a["rows"]) == total,
          f"{len(a['sels'])} + {len(a['rows'])} == {total} projects")
    check(not a["empty"], "no empty-state message")
    check(a["pressed"] == ["all"], f"aria-pressed on exactly All: {a['pressed']}")
    # Named explicitly, because an empty label list makes every label check
    # below vanish without a word -- which is how a renamed class walks past a
    # green run.
    check(sorted(l["id"] for l in a["labels"]) == ["proj-lab-idx", "proj-lab-sel"],
          f"both tier labels found: {[l['id'] for l in a['labels']]}")
    for lab in a["labels"]:
        want = len(a["sels"]) if lab["id"] == "proj-lab-sel" else len(a["rows"])
        check(lab["count"] == str(want) and not lab["hidden"],
              f"{lab['id']} reads {lab['count']}, wants {want}")
    for btn in buttons[1:]:
        name, want = btn["name"], btn["count"]
        s = states[name]
        shown = s["sels"] + s["rows"]
        print(f"\n{name} (button says {want})")
        check(len(shown) == want, f"{len(shown)} visible, button says {want}")
        check(s["pressed"] == [name], f"aria-pressed on exactly {name}: {s['pressed']}")
        check(s["empty"] == (len(shown) == 0), "empty-state message matches")
        for lab in s["labels"]:
            want_n = len(s["sels"]) if lab["id"] == "proj-lab-sel" else len(s["rows"])
            check(lab["count"] == str(want_n) and lab["hidden"] == (want_n == 0),
                  f"{lab['id']} reads {lab['count']} and is "
                  f"{'hidden' if lab['hidden'] else 'shown'}, wants {want_n}")
        check(len(set(shown)) == len(shown), "no project listed twice")

    # The should-fail side: a project must disappear from filters it does not
    # carry. A check that only ever asserts presence cannot catch a filter that
    # does nothing.
    print("\nabsence")
    everywhere = set.intersection(*[set(states[b["name"]]["sels"] + states[b["name"]]["rows"])
                                    for b in buttons[1:]]) if len(buttons) > 1 else set()
    check(not everywhere,
          f"no project survives every filter (found: {sorted(everywhere)})")

    # The homepage links straight to /projects/#<capability>, so the filter has
    # to survive being read off the URL rather than clicked.
    print("\nlanding on #tools")
    deep = collect(args.url, "#tools")["initial"]
    tools = states["tools"]
    check(deep["pressed"] == ["tools"], f"arrives with tools pressed: {deep['pressed']}")
    check(deep["sels"] == tools["sels"] and deep["rows"] == tools["rows"],
          "shows the same projects as clicking Tools")

    print("\nlanding with no fragment")
    check(data["initial"]["pressed"] == ["all"], "opens on All")

    print("\nback to all")
    b = states["all-again"]
    check(b == states["all"], "returning to All restores the opening state")

    print()
    if fails:
        print(f"{len(fails)} failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
