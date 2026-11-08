# ADHD Planner — Free 10-Page Trial

A hyperlinked digital planner for adults with ADHD and executive-function
challenges. Built for iPad apps like GoodNotes and Notability: tap a link,
jump to the page.

This repository holds a **free 10-page trial**. The full planner will be
built and released only after the trial passes validation.

## What's inside the trial

1. **Cover** — what this planner is
2. **Index** — tap a section to jump to it
3. **Daily Plan** — top 3, time blocks, one win
4. **Weekly Plan** — one focus per day, and what can wait
5. **Brain Dump** — catch every thought, sort it later
6. **Task Breakdown** — one big task into tiny steps
7. **Dopamine Menu** — quick rewards, ready before you need them
8. **Low-Pressure Tracker** — track without punishing streaks
9. **Month Overview** — the whole month on one calm page
10. **How to Use** — import steps and the three rules

Page size is 768 × 1024 pt (GoodNotes import size). All 25 internal links
were verified with `validate_pdf.py` — 0 broken.

## How to use

1. Download `adhd-planner-trial-10pages.pdf`.
2. Import it into GoodNotes or Notability.
3. Tap **Index** at the top of any page to go back, or **Next** to move
   forward. Duplicate daily and weekly pages whenever you need a fresh copy.

## Trial validation

This trial is free for 7 days of download testing. If it reaches **20 or
more downloads**, the full planner gets built. The full version's sales
link (Gumroad) is still to be decided and will be added here when ready.

## Build it yourself

```bash
pip install reportlab pypdf
python3 build_pdf.py        # writes adhd-planner-trial-10pages.pdf
python3 validate_pdf.py     # checks page count, links, and file size
```

- `build_pdf.py` — generates the PDF (original layout and copy).
- `validate_pdf.py` — verifies all internal links resolve and every page
  is reachable.

## License

MIT — see [LICENSE](LICENSE).
