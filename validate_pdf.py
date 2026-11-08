#!/usr/bin/env python3
"""Validate the ADHD Planner trial PDF.

Checks (fail loudly, exit non-zero on any failure):
  1. Page count is exactly 10.
  2. Every internal link annotation resolves to an existing page
     (reportlab writes explicit [page /XYZ ...] destinations; named
     destinations are resolved the same way when present).
  3. Every page 2-10 is the target of at least one link (page 1 is the
     entry point, reached by opening the file).
  4. File size is reasonable (< 5 MB).

Usage: python3 validate_pdf.py [pdf-path]
Requires: pypdf.
"""

import os
import sys

from pypdf import PdfReader

EXPECTED_TARGET_PAGES = set(range(2, 11))  # pages 2-10 must each be a link target;
# page 1 (cover) is the entry point, reached by opening the file.
MAX_BYTES = 5 * 1024 * 1024


def resolve_dest(reader, annot, page_no):
    """Return (ok, detail, target_page_or_None) for one link annotation.

    Note: reportlab resolves bookmark names to explicit [page /XYZ ...]
    destinations at save time, so pypdf sees explicit destinations, not
    named ones. We therefore resolve the target page object directly.
    """
    obj = annot.get_object()
    if obj.get("/Subtype") != "/Link":
        return None  # not a link annotation
    dest = None
    action = obj.get("/A")
    if action is not None:
        action = action.get_object()
        if action.get("/S") == "/GoTo":
            dest = action.get("/D")
    if dest is None:
        dest = obj.get("/Dest")
    if dest is None:
        return (False, f"page {page_no}: link annotation has no destination", None)
    if isinstance(dest, str):
        named = reader.named_destinations
        if dest in named:
            target = named[dest]
            try:
                page_obj = target[0].get_object()
            except Exception:
                page_obj = None
            for i, p in enumerate(reader.pages):
                if page_obj is not None and p.get_object() is page_obj:
                    return (True, f"page {page_no}: named dest '{dest}' -> page {i + 1} OK", i + 1)
            return (True, f"page {page_no}: named dest '{dest}' OK (page not traced)", None)
        return (False, f"page {page_no}: named dest '{dest}' MISSING", None)
    # Explicit destination array: first element is the target page object.
    try:
        dest = dest.get_object()
        target = dest[0].get_object()
        for i, p in enumerate(reader.pages):
            if p.get_object() is target or p == target:
                return (True, f"page {page_no}: explicit dest -> page {i + 1} OK", i + 1)
        return (False, f"page {page_no}: explicit dest points to unknown page", None)
    except Exception as exc:  # noqa: BLE001 - report, don't crash
        return (False, f"page {page_no}: unresolvable dest ({exc!r})", None)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "adhd-planner-trial-10pages.pdf")
    errors = []
    reader = PdfReader(path)
    n_pages = len(reader.pages)
    print(f"File: {path}")
    print(f"Size: {os.path.getsize(path)} bytes")
    print(f"Pages: {n_pages} (expected 10)")
    if n_pages != 10:
        errors.append(f"page count {n_pages} != 10")
    if os.path.getsize(path) > MAX_BYTES:
        errors.append(f"file too large: {os.path.getsize(path)} bytes > {MAX_BYTES}")

    named = set(reader.named_destinations.keys())
    print(f"Named destinations in file: {sorted(named)} (reportlab resolves "
          f"bookmarks to explicit page destinations; empty is expected)")

    total_links = 0
    broken = 0
    targets = set()
    for i, page in enumerate(reader.pages):
        annots = page.get("/Annots") or []
        for annot in annots:
            result = resolve_dest(reader, annot, i + 1)
            if result is None:
                continue
            total_links += 1
            ok, detail, target_page = result
            if target_page is not None:
                targets.add(target_page)
            if not ok:
                broken += 1
                errors.append(detail)
    print(f"Internal links: total={total_links} broken={broken}")
    print(f"Link target pages: {sorted(targets)} (expected {sorted(EXPECTED_TARGET_PAGES)})")
    if total_links == 0:
        errors.append("no internal links found at all")
    missing_targets = EXPECTED_TARGET_PAGES - targets
    if missing_targets:
        errors.append(f"pages never targeted by any link: {sorted(missing_targets)}")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
