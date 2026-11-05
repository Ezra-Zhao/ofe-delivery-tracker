# OFE Expediting Playbook

> **SIMULATED CONTEXT.** The worked examples reference the fictional items in
> `data/ofe_line_items.csv` (OFE-003, OFE-010, OFE-025). The methods are real
> delivery practice; the items, sites, and dates are invented.
>
> **Source note for the receiving section (Section 5 only):** the receiving,
> storage, and preservation checklist migrates the author's real experience as
> the *receiving side* in data center operations (Asiacom, a roughly 1,000-rack
> facility) - what the operations receiver wishes the delivery side had checked
> before the truck arrived. That experience is real; this checklist, like the
> rest of the playbook, is a methodology artifact written for this repository
> and was not used on a real OFE program. The same source-separation labelling
> is used in the companion dc-delivery-playbook turnover checklist.

## 1. Weekly OEM cadence

One call per active supplier per week, run off the tracker - never off the
supplier's own status deck.

Agenda (30 minutes, fixed order):

1. **Slot verification** - every line item in production: where is the unit
   physically in build, against the committed production slot in the tracker?
2. **Milestone deltas** - any movement in submittal, FAT, ship, or ROS dates
   since last week. Movement without a reason is treated as no information.
3. **Constraint disclosure** - components, test-bay capacity, labor, freight.
   Asked explicitly, every week, even when dates hold (see Section 2).
4. **Recovery commitments** - for every drifting item: the recovery action,
   its owner by name, and the date it will be visible in the tracker.
5. **Two-week lookahead** - FATs and shipments in the next 14 days, with
   witness/notification arrangements confirmed.

Ground rules: the tracker is updated during the call, not after it; a date
that changes gets its reason recorded in the notes field the same day; "on
track" is not an acceptable status for any milestone inside its lead-time
window.

## 2. Verification questions (verify production, do not accept reported dates)

The discipline: a date is a claim until something physical or documentary
verifies it. Asked in this order:

- "Which build stage is the unit in today, and what is the stage exit
  criterion?" (A percent-complete answer is not evidence; a stage with an
  exit test is.)
- "Show me the slot: is this unit's production slot still the one in our
  tracker, or has it been re-sequenced behind another customer's unit?"
- "What is the longest-lead component for this unit, where is it right now -
  in your plant, in transit, or still at your sub-supplier?"
- "For the FAT: what is the test procedure reference, who witnesses, and what
  were the results on the last unit of this type you tested?"
- "What has to be true on your side for the ship date to hold - and which of
  those things is least in your control?"
- "If I call next week and the date has moved, what will the reason most
  likely be?" (Asked while things are calm, this question surfaces the real
  constraint early.)

Evidence accepted, in descending order of trust: FAT/test records with unit
serial numbers; dated production photos tied to serial numbers; sub-supplier
shipping confirmations; carrier booking references. Not accepted as sole
evidence: a revised spreadsheet, a percent-complete figure, "should ship".

## 3. Slip recovery decision tree

Trigger: any item whose forecast ROS drifts past plan, or whose next
milestone misses.

Step 1 - **Verify before reacting.** Run Section 2. If the slip is a
reporting artifact (date moved, unit did not), correct the tracker and stop.

Step 2 - **Quantify the blast radius.** Is this ROS on the critical path for
energization / commissioning, or is there float? What downstream work
(installation crew, GC sequence, Cx levels) actually moves?

Step 3 - **Pick the recovery lever, in this order:**

| Lever | Use when | Watch out for |
|---|---|---|
| Expedite inside the factory (overtime, slot swap within the same OEM) | Constraint is factory capacity or sequencing; unit is built or in build | Premium cost needs a named approver; confirm the new slot in writing the same day |
| Partial / split shipment | The order has multiple units and the site needs the first units to start installation; remaining units can follow | Split must not break a matched set (e.g. paralleling gear vs generators); extra freight and double receiving effort |
| Resequence site work | There is float elsewhere: another hall, another equipment train, or fit-out work that can go first | Resequencing is borrowing float, not creating it; record what float was consumed in the decision log |
| Alternate source (with Sourcing) | The OEM cannot recover inside the schedule need, and the category has a qualified second source | Commercial terms and submittal re-approval take real time; this is a Sourcing-led decision - delivery supplies the schedule evidence, not the commercial call |
| Accept and re-baseline | No lever recovers the date and float is genuinely gone | Only through the decision log, with leadership seeing baseline vs forecast; never by silently editing the planned ROS |

Step 4 - **Report one converged picture.** Slip, options, cost of each, the
decision needed and by when. Not a stream of status updates.

Worked examples (simulated items):

- **OFE-003, transformer, factory delay (+35 d):** verify the slot claim at
  the OEM plant (which stage, which component - core steel), check whether
  TX-1's already-delivered train lets energization resequence, then escalate
  commercially with that evidence (Section 4). Alternate sourcing a 40MVA
  transformer inside 35 days is not credible - do not pretend otherwise in
  the report; say so and show the resequence math instead.
- **OFE-010, CDU, FAT fail (+28 d):** the recovery clock is rework plus
  retest, not shipping. Get the failure record (which loop, which alarm),
  the rework plan, and a retest slot with witness arrangements before
  accepting any new date; hold the ship date field empty until retest passes.
- **OFE-025, chiller, logistics delay (+28 d):** the unit exists - the
  constraint is route permit and port congestion. Levers are route re-survey,
  alternate port/carrier, and resequencing installation to the second
  chiller's train; factory expediting buys nothing here.

## 4. Escalation ladder

| Level | Forum | Trigger | Product |
|---|---|---|---|
| L1 Site delivery | Weekly cadence with the OEM's program contact | Any milestone drift, any unanswered verification question | Updated tracker, named recovery action and date |
| L2 Program | Delivery lead + OEM account management | Drift > 14 d, or the same item drifts twice, or a FAT failure | Written recovery plan with slot/test evidence |
| L3 Sourcing / commercial | Sourcing partner escalates under the contract | Recovery plan missed, or commercial commitments (LDs, priority allocation) are the lever | Commercial escalation record; delivery side supplies the verified schedule evidence |
| L4 Leadership | Capacity Delivery Review | Ready-for-service date moves, or re-baselining is proposed | One-page decision: options, costs, recommendation (see the portfolio risk report format) |

Rules: an item never sits at one level for more than two cadence cycles
without moving up or closing; escalation cycle time is a tracked KPI (see
`src/ofe_kpi.py`), because a slow ladder is a schedule risk of its own; the
delivery role owns the evidence at every level - commercial ownership stays
with Sourcing, and this playbook does not pretend otherwise.

## 5. Receiving, storage, and preservation checklist

(Source note at the top of this file applies to this section: receiving-side
experience, migrated as method.)

Run at ROS, with the GC's OFCI receiving team, before the item is accepted:

Receiving:

- [ ] Advance shipping notice reconciled against the tracker line item
      (model, serial numbers, quantity) before the truck is unloaded.
- [ ] Visible transit damage inspection with photos before signing; damage
      noted on the delivery receipt, not in a later email.
- [ ] Nameplate data photographed and checked against the approved submittal -
      the receiving dock is the last cheap place to catch a wrong-variant unit.
- [ ] Rigging path and laydown location confirmed before arrival for
      oversize/overweight units (crane window, route, floor loading).

Storage and preservation:

- [ ] OEM preservation requirements pulled from the O&M documentation on day
      one: desiccant/space heaters energized for electrical gear, nitrogen
      blanket or oil condition for transformers, shaft rotation schedule for
      rotating equipment, battery float/refresh for UPS strings.
- [ ] Preservation log started at receiving - a preserved unit with no log is
      treated as unpreserved at turnover.
- [ ] Laydown area conditions recorded (indoor/outdoor, humidity control,
      security); deviations from OEM storage conditions escalated the same
      week, because they can void warranty.
- [ ] Warranty start basis confirmed in writing: shipment, delivery, or
      start-up - the difference is real money and is decided at receiving,
      not at claim time.

Installation-readiness handoff:

- [ ] Installation crew confirms foundation/anchoring, clearances, and
      utility stub-ups match the approved submittal drawings before the unit
      leaves laydown.
- [ ] Accessories and loose-shipped parts inventoried against the packing
      list; shortages raised while the carrier claim window is still open.
- [ ] Item status flipped in the tracker (delivered, accepted, preserved)
      the same day - the tracker stops being true the first time receiving
      happens off-record.
