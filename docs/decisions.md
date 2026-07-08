# Decision Log (ADR-lite)

Every "Open Question" from the vault note gets resolved here with a dated entry.
These become the design-decision paragraphs in the final write-up.

Format per entry:

```
## D-NNN: <title>
- **Date:** YYYY-MM-DD
- **Phase:** N
- **Decision:**
- **Reasoning:**
- **Alternatives considered:**
```

---

## Open questions to resolve (from the vault note / implementation guide)

- [ ] **D-001 — Eval subset size & stratification** (Phase 0): how many questions,
      stratified how, and what confidence interval does that N buy? (Rule of thumb: ±1/√N.)
- [ ] **D-002 — BIRD "evidence" field** (Phase 0): does the agent get to see the
      evidence hints? Same answer for all conditions?
- [ ] **D-003 — `get_schema` output format** (Phase 1): full DDL dump vs. compact
      formatted schema. Token cost differs a lot — measure in Phase 3.
- [ ] **D-004 — SQL extraction convention** (Phase 2): fenced code block vs. a
      `submit_sql` final-tool convention.
- [ ] **D-005 — Does repair deserve its own condition row?** (Phase 2/3): answer
      empirically once condition 3 vs 4 numbers exist.
- [ ] **D-006 — Temperature / determinism** (Phase 3): decide and log; temp > 0
      interacts with K in Pass@K.
- [ ] **D-007 — Failure-taxonomy legibility** (Phase 3): which buckets, and are they
      legible to a hiring audience?
- [ ] **D-008 — Judge model choice** (Phase 4): frontier judge vs. smaller model —
      run both on a 30-question sample, measure agreement with hand labels.
- [ ] **D-009 — Prompt freeze point** (Phase 3): date/commit at which tool
      descriptions + system prompts were frozen before the full run.

---

<!-- Resolved decisions go below, newest last -->
