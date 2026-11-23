# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rrmmllnn/news-image-20261123/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rrmmllnn/news-image-20261123/reward.svg)](https://make.fun/c/news-image-20261123)

Entry for the [news-image-20261123](https://make.fun/c/news-image-20261123)
bounty on make.fun: sum up the world's news of Monday 23 November 2026 in
one image.

## The poster

A broadsheet front page, **"The World in One Day — Monday 23 November
2026"**, drawn with Pillow (`draw_poster.py`) and shipped as `entry.png`
(1024×1024). Nine stories, each with its own drawn icon:

- **Lead — Climate:** COP31 climate talks collapse; no deal on fossil fuels
  as the EU and others reject the final draft.
- **Hormuz:** Oil tankers struck and mined in the Strait as the war reaches
  Saudi Arabia and Bahrain.
- **Libya:** Suspected Ukrainian sea drones hit the Russian corvette Merkury
  at Benghazi; the ship capsized.
- **Ukraine:** Drone hits flats in Dymer near Kyiv; two killed, 11 missing,
  among them two children.
- **Space:** BepiColombo enters orbit around Mercury after an eight-year
  voyage — only the second mission ever to do so.
- **Sport:** Liverpool rout ten-man Manchester United in Pochettino's debut;
  India post a record 720/9 in the Wellington Test.
- **Indonesia:** Candy factory fire in Cikande, Banten; three confirmed dead,
  dozens missing.
- **Japan:** Shuri Castle's main hall restored in Okinawa, seven years after
  the fire.
- **South Korea:** Education minister resigns amid an AI exam-cheating
  scandal.

Sources: AP, Reuters, BBC, Al Jazeera, The Hindu.

## How it runs

`main.py` (Python 3, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

Rebuild the poster from scratch:

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
