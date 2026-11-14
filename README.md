# mrbricolage-unofficial

The wood panels Mr.Bricolage France lists, as data for [furniture-design](https://github.com/xag/furniture-design). **Unofficial**: Mr.Bricolage did not write or endorse it, and nothing here speaks for it.

## What is here

- **The range**: 741 products read from Mr.Bricolage's public product sitemap (https://www.mr-bricolage.fr/media/sitemap/sitemap_mr_bricolage.xml), each with its line, thickness, sheet size and address, in 21 lines (agglomere, agglomere-hydrofuge, contreplaque, contreplaque-okoume, contreplaque-peuplier, lamelle-colle-chene, lamelle-colle-hetre, lamelle-colle-pin, lamelle-colle-sapin, massif-chene, massif-hetre, massif-peuplier, massif-pin, massif-sapin, massif-sapin-du-nord, mdf, mdf-hydrofuge, melamine, osb, osb-3, panneau-3-plis). What a given store has in stock is not in the sitemap.
- **The materials**: one per line and thickness (`materials/mrbricolage-<line>-<thickness>`), two for a board that bends differently along and across. [wood-panels](https://github.com/xag/wood-panels)'s `shops` module reads the titles and gives each line its values: a class's (P2, P3, MDF, OSB/3), a maker's board of the same type, or a species of furniture-design, all ungrounded unless the title names the class or the maker; the payload `shop` says what is sold and which board the values are.

No kinds and no rules of its own: a part that `uses` one of these materials is judged by furniture-design's rules.

## Sources

The sitemap's entries as fetched on 2026-11-14 are kept in a private repo with the sha256 of each sitemap file, and `tests/test_values.py` checks that every product is an entry and reads as its row: clone that repo beside this one, or set `FURNITURE_REPO`, or that test fails and says why. `tools/read_range.py` reads the range again from a folder of sitemap files.

## Using it

```python
from furniture_design.knowledge import knowledge as general, merge
from wood_panels import knowledge as wood_panels
from mrbricolage_unofficial import knowledge as mrbricolage

tree.root.children = merge(general(), wood_panels(), mrbricolage()) + [pieces]
```

## Design ledger

```sh
uv sync
uv run quern brief .
uv run quern check
```

There is no flight-recorder boundary: nothing here touches storage, the network, the clock or randomness at run time.

## Licence

- **The code** (`mrbricolage_unofficial/*.py`, `tools/`, `tests/`, `ledger/`) is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE), copyright 2026 Xavier Grehant.
- **The knowledge base**, the database `mrbricolage_unofficial.knowledge()` returns (range.json and every value on its nodes), is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](LICENSE-DATA), database rights included, with one added permission: designing, building and selling furniture with it is allowed. An improvement is published here, through [CONTRIBUTING.md](CONTRIBUTING.md).
- Mr.Bricolage's product names and sizes are cited from its sitemap, not licensed.

## Tests

`uv run pytest --testmon`, then `uv run pytest`. Both stop at the first failure.
