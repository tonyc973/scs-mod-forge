# Acceptance checklist (close a round only when all are ✅ or explicitly deferred)

## Evidence
- [ ] Every item has **in-game** screenshots from the agreed views (not Blender renders).
- [ ] Each screenshot is placed **next to its reference** (side-by-side or overlay).
- [ ] Each change has a **before/after** pair; changes that were not clearly better were **reverted**.

## Correctness
- [ ] The diagnosis (root cause) is written for every item.
- [ ] `mesh_audit.py` is clean on every touched object (no non-manifold edges, concave n-gons or flipped normals).
- [ ] Measured targets are met (gaps, overlay deviation, timings).
- [ ] No invented `.sii` attributes: every attribute used appears in vanilla files or the SCS wiki.

## Non-regression
- [ ] Systems marked "do not touch" were not modified (or the reason is documented).
- [ ] Open items from earlier rounds are either visible in game or carried forward explicitly.

## Housekeeping
- [ ] Diagnostic builds (`*_diag`) were deleted and not shipped.
- [ ] Old parts were moved to `OLD_vN`, not deleted.
- [ ] Third-party references are only linked; no copyrighted images or sounds are in the mod.
- [ ] Questions for the real-vehicle owner are listed.
