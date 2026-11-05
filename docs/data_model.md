# OFE Line-Item Data Model

> **SIMULATED DATA.** The dataset in `data/ofe_line_items.csv` is fictional
> (two invented sites, invented orders and dates). It exists to exercise this
> model and the KPI code. No real employer, customer, purchase order, or
> delivery data is used anywhere in this repository.

## Purpose

One row = one OFE (owner-furnished equipment) line item, tracked from purchase
order to ready-on-site (ROS). The model is the "single source of truth" the
OFE delivery role runs: every milestone the job description names - order
placement, submittal/approval, production slot, FAT, ship, ROS - is a field,
not a sentence in a status email.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `line_item_id` | string | Stable key, `OFE-NNN`. Never reused. |
| `site` | string | Delivery site. Simulated values: `HELIOS-ALPHA`, `HELIOS-BETA`. |
| `equipment_category` | enum | One of the JD categories: Switchgear, Transformers, UPS, Generators, Busway, PDUs, Chillers, CDUs, Air Handlers. |
| `equipment_description` | string | Human-readable unit description (nameplate level, not marketing level). |
| `supplier` | string | OEM supplying the unit (simulated assignments). |
| `quantity` | int | Units on this line item. |
| `po_date` | date | Purchase order placement date. Chain start. |
| `submittal_status` | enum | `Submitted`, `In review`, `Approved`. Anything not `Approved` blocks production-slot confidence. |
| `submittal_approval_date` | date, nullable | When the submittal was approved. Empty until approved. |
| `production_slot_start` / `production_slot_end` | date | The OEM factory slot committed for this unit. This is the date set the weekly cadence verifies against - see the playbook. |
| `fat_date` | date, nullable | Factory Acceptance Test date (scheduled or held). |
| `fat_result` | enum | `Pass`, `Fail`, `Not yet`. A `Fail` must carry an open escalation and no ship date. |
| `ship_date` | date, nullable | Actual ship date. Empty until the unit physically leaves the factory. |
| `ros_date_planned` | date | Baseline required-on-site date, integrated with the GC construction schedule. The baseline does not move silently; changes go through the decision log discipline. |
| `ros_date_forecast` | date | Current forecast ROS. For delivered items this equals the final actual. Drift is measured from this field so open items count too. |
| `ros_date_actual` | date, nullable | Actual arrival-on-site date. Present only for delivered items. |
| `risk_rating` | enum | `Low`, `Medium`, `High`. High requires an open or closed escalation trail. |
| `escalation_status` | enum | `None`, `Open`, `Closed`. |
| `escalation_open_date` / `escalation_close_date` | date, nullable | Escalation window; cycle time is computed from closed pairs only. |
| `scenario` | string | Demonstration tag. Three rows carry `SLIP-FACTORY-DELAY`, `SLIP-FAT-FAIL`, `SLIP-LOGISTICS`; all other rows are empty. |
| `notes` | string | One-line factual note. Facts, not adjectives. |

## KPI definitions (implemented in `src/ofe_kpi.py`)

- **drift_days** = `ros_date_forecast - ros_date_planned` (positive = late).
- **On-time-to-ROS** = delivered items with `ros_date_actual <= ros_date_planned`,
  divided by delivered items. Open items are excluded on purpose: a forecast is
  not a delivery.
- **Forecast on-time rate** = items with drift <= 0, divided by all items.
  Reported next to on-time-to-ROS so forecast optimism is visible.
- **Drift by supplier / by category / by site** = count, mean drift, max drift,
  late-item count per group.
- **Escalation cycle time** = close minus open date over closed escalations;
  open escalations are listed by ID, never averaged in.

## Invariants the tests enforce

1. 40 rows; exactly 20 per site.
2. Category set equals the nine JD categories - no more, no less.
3. Exactly three slip scenarios, one of each type; each has drift > 0,
   risk = High, escalation = Open.
4. A `Fail` FAT row has no ship date and no actual ROS.
5. Every row has a planned and a forecast ROS; actual ROS appears only on
   delivered rows (29 in this snapshot).
