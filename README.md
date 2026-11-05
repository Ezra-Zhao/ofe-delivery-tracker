# ofe-delivery-tracker - proof artifact

> **SIMULATED DATA - FIRST SCREEN NOTICE.** Every site, line item, date,
> order, and result in this repository is fictional and simulated. Nothing
> here describes a real project, a real employer program, or real deliveries.
> Supplier names appear only as illustrative OEM assignments inside the
> simulated dataset.

## What this is

A working, runnable model of the delivery system for owner-furnished
equipment (OFE) on data center construction: a line-item tracker covering
the full chain - purchase order, submittal/approval, production slot, FAT,
ship, required-on-site (ROS) - plus the KPI computation and the expediting
playbook that run on top of it.

It was built against the Anthropic Supply Chain Delivery Manager, Data
Center Power & Cooling OFE job description, whose own words define the
artifacts: a live tracker as the single source of truth, verification of
production progress against committed slots rather than accepting reported
dates at face value, and KPIs including on-time-to-ROS, schedule drift by
supplier and category, and escalation cycle time.

## What it proves / does not prove

- **Proves:** milestone-chain management method (PO to ROS with gated
  milestones), the verify-don't-trust status discipline, data fluency
  (tracker design, KPI computation, one-page risk reporting), and a slip
  recovery method (expedite / partial ship / resequence / alternate source)
  that can be walked through end to end on the simulated data.
- **Does not prove:** that the author has delivered OFE equipment categories
  (switchgear, transformers, UPS, generators, chillers, CDUs) on a real
  program. The equipment-category delivery record does not exist and is not
  claimed anywhere in this repository. Category knowledge is being studied
  separately (learning plan item P52); this artifact proves the management
  method that transfers, not category delivery history.

## Method sources (what is migrated, and from where)

- The verification discipline (a date is a claim until something physical or
  documentary verifies it) migrates the author's real working method from
  manufacturing program engineering: pushing back on design decisions with
  build-floor evidence, and data-driven fault diagnosis in operations.
  **Method only - no employer data, dates, or figures are used.**
- The receiving/storage/preservation checklist in the playbook migrates the
  author's real experience as the receiving side in data center operations.
  It is labelled separately inside `docs/expediting_playbook.md`, following
  the same source-separation labelling as the dc-delivery-playbook turnover
  checklist.
- Nothing in this repository contains interview-invented lead times presented
  as fact. Simulated dates exist only inside the clearly labelled simulated
  dataset and are never stated as real category lead times.

## Contents

| Path | Content |
|---|---|
| `data/ofe_line_items.csv` | Simulated dataset: 40 line items, 2 fictional sites (20 each), 9 JD equipment categories, 3 tagged slip scenarios (factory delay, FAT fail, logistics delay) |
| `docs/data_model.md` | Field-by-field data model, KPI definitions, dataset invariants |
| `src/ofe_kpi.py` | KPI computation: on-time-to-ROS, forecast on-time, drift by supplier/category/site, escalation cycle time, risk summary |
| `src/generate_report.py` | One-command generator for the one-page portfolio risk report |
| `reports/portfolio_risk_report.md` | Generated one-page report (Capacity Delivery Review format) |
| `docs/expediting_playbook.md` | Weekly OEM cadence, verification question set, slip recovery decision tree, escalation ladder, receiving/storage/preservation checklist |
| `tests/test_kpi.py` | pytest suite pinning dataset shape and KPI behaviour |
| `VERIFICATION.md` | Build verification record: commands run and results |

## Run it

```bash
cd ~/workspace/ofe-delivery-tracker
python3 src/generate_report.py     # prints KPI JSON, writes reports/portfolio_risk_report.md
python3 -m pytest tests/ -q        # test suite (pytest; see VERIFICATION.md for environment note)
```

## Increment vs dc-delivery-playbook (zero overlap statement)

The dc-delivery-playbook is **site-level**: a CPM master schedule, risk
register, and turnover gate for one fictional site build. This artifact is
**equipment-line-level**: the procurement-to-dock chain, supplier/category
drift analysis, and expediting practice. Scheduling object, data grain, and
KPI set are all different; the only shared element is the general
risk/decision recording discipline. No content is copied from it.
