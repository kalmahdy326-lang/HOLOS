# HOLOS Episode 1 — Final Render Verification Rules

This page is a concise entry point, not a replacement checklist. Follow the complete [Final Render Verification protocol](final_render_verification.md) and record decisions in the [Final Verification Checklist](final_verification_checklist.md).

A successful render command, passing CI, or valid metadata alone does not establish acceptance. Before rendering, lock an approved, versioned delivery profile. Derive dimensions, frame rate/timebase, codecs, audio settings, color, and tolerances from that profile; do not assume defaults or claim compliance without measured evidence.

Acceptance requires **both**:

- **Automated gates:** exact-hash input/profile traceability; expected frames/order/decoding; profile-conformant metadata, duration, stream layout, audio and timing; retained reports/logs and archive integrity.
- **Independent human gates:** named reviewer examines the exact candidate, completes uninterrupted full-program playback, reviews visual/audio quality and perceptual sync, checks subtitles/credits and defects, and records disposition; authorized delivery/rights approvers sign the same hash.

Every applicable check must pass on the same exact hashes before `COMPLETE`. Changed inputs or output require affected revalidation and review. Missing, failed, unresolved, or hash-mismatched evidence blocks acceptance.

**Evidence boundary:** No full-body render is evidenced as verified; no full episode is verified. This rules page does not assert that any render or review has passed. See the detailed protocol for scope, criteria, records, change control, and archive requirements.
