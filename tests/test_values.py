"""The range against the sitemap entries it was read from, and the data against furniture-design's rules.

The entries are kept in the private repo xag/furniture, checked out beside this one (or at $FURNITURE_REPO),
under sources/mrbricolage/. Without them these tests fail, saying where they looked, and never skip.
"""

import hashlib
import json
import os
from pathlib import Path

from quern import Quern, run_rules

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from wood_panels import knowledge as wood_panels
from wood_panels.shops import LINES, problems
from mrbricolage_unofficial import knowledge, rows

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "mrbricolage"


def _here(path: Path) -> Path:
    assert path.exists(), (f"the private copy {path} is missing: clone xag/furniture beside this repo or "
                           "set FURNITURE_REPO")
    return path


def test_every_product_is_its_sitemap_entry_and_reads_as_its_row():
    captured = json.loads(_here(CAPTURES / "sitemap-entries.json").read_text(encoding="utf-8"))
    assert problems(rows(), captured) == []
    assert captured["sitemaps"] and all(len(s) == 64 for s in captured["sitemaps"].values())


def test_every_line_the_range_names_is_described():
    assert {r["line"] for r in rows()} <= {line.id for line in LINES}


def test_no_two_materials_share_an_id():
    ids = [m.id for b in knowledge() if b.id == "materials" for m in b.children]
    assert len(ids) == len(set(ids))


def test_the_data_passes_furniture_designs_rules():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), wood_panels(), knowledge())
    assert [(r.rule, r.node, r.verdict) for r in run_rules(tree) if not r.ok] == []
