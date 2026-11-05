"""OFE delivery tracker - KPI computation.

SIMULATED DATA ONLY. All line items in data/ofe_line_items.csv are fictional,
created to demonstrate the tracking and KPI method described in the Anthropic
Supply Chain Delivery Manager (OFE) job description:
  - on-time-to-ROS
  - schedule drift by supplier and by category
  - escalation cycle time

Definitions (kept deliberately simple and auditable):
  - drift_days(item) = ros_date_forecast - ros_date_planned, in days.
    For delivered items ros_date_forecast equals the final forecast, which by
    construction in this dataset equals ros_date_actual.
  - On-time-to-ROS counts only delivered items (ros_date_actual present):
    on time when ros_date_actual <= ros_date_planned.
  - Forecast on-time rate covers all items, using ros_date_forecast.
  - Escalation cycle time covers closed escalations only:
    escalation_close_date - escalation_open_date, in days.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from statistics import mean

DATE_FIELDS = (
    "po_date", "submittal_approval_date", "production_slot_start",
    "production_slot_end", "fat_date", "ship_date", "ros_date_planned",
    "ros_date_forecast", "ros_date_actual", "escalation_open_date",
    "escalation_close_date",
)


def _parse_date(value: str | None) -> date | None:
    value = (value or "").strip()
    return date.fromisoformat(value) if value else None


def load_items(path: str | Path) -> list[dict]:
    """Load line items, parsing date fields to datetime.date (or None)."""
    items = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            item = dict(row)
            for field in DATE_FIELDS:
                item[field] = _parse_date(row.get(field))
            item["quantity"] = int(row["quantity"])
            items.append(item)
    return items


def drift_days(item: dict) -> int:
    """Forecast ROS drift vs planned ROS, in days (positive = late)."""
    return (item["ros_date_forecast"] - item["ros_date_planned"]).days


def on_time_to_ros(items: list[dict]) -> dict:
    """On-time-to-ROS over delivered items only."""
    delivered = [i for i in items if i["ros_date_actual"] is not None]
    on_time = [i for i in delivered if i["ros_date_actual"] <= i["ros_date_planned"]]
    return {
        "delivered": len(delivered),
        "on_time": len(on_time),
        "rate": (len(on_time) / len(delivered)) if delivered else None,
    }


def forecast_on_time(items: list[dict]) -> dict:
    """Forecast on-time rate over all items (forecast ROS vs planned ROS)."""
    on_time = [i for i in items if drift_days(i) <= 0]
    return {
        "total": len(items),
        "on_time_forecast": len(on_time),
        "rate": (len(on_time) / len(items)) if items else None,
    }


def _drift_group(items: list[dict], key: str) -> dict:
    groups: dict[str, list[int]] = {}
    for item in items:
        groups.setdefault(item[key], []).append(drift_days(item))
    return {
        name: {
            "count": len(values),
            "mean_drift_days": round(mean(values), 1),
            "max_drift_days": max(values),
            "late_items": sum(1 for v in values if v > 0),
        }
        for name, values in sorted(groups.items())
    }


def drift_by_supplier(items: list[dict]) -> dict:
    return _drift_group(items, "supplier")


def drift_by_category(items: list[dict]) -> dict:
    return _drift_group(items, "equipment_category")


def drift_by_site(items: list[dict]) -> dict:
    return _drift_group(items, "site")


def escalation_cycle_time(items: list[dict]) -> dict:
    """Cycle time for closed escalations; open ones are counted separately."""
    closed, open_items = [], []
    for item in items:
        if item["escalation_status"] == "Closed":
            days = (item["escalation_close_date"] - item["escalation_open_date"]).days
            closed.append({"line_item_id": item["line_item_id"], "cycle_days": days})
        elif item["escalation_status"] == "Open":
            open_items.append(item["line_item_id"])
    cycles = [c["cycle_days"] for c in closed]
    return {
        "closed_count": len(closed),
        "mean_cycle_days": round(mean(cycles), 1) if cycles else None,
        "max_cycle_days": max(cycles) if cycles else None,
        "closed": closed,
        "open_items": open_items,
    }


def risk_summary(items: list[dict]) -> dict:
    """Counts by risk rating and by open high-risk items."""
    counts: dict[str, int] = {}
    for item in items:
        counts[item["risk_rating"]] = counts.get(item["risk_rating"], 0) + 1
    open_high = [
        i["line_item_id"] for i in items
        if i["risk_rating"] == "High" and i["escalation_status"] == "Open"
    ]
    return {"by_rating": counts, "open_high_risk": open_high}


def slip_scenarios(items: list[dict]) -> list[dict]:
    """Items carrying an explicit slip scenario tag."""
    return [
        {
            "line_item_id": i["line_item_id"],
            "scenario": i["scenario"],
            "site": i["site"],
            "equipment_category": i["equipment_category"],
            "supplier": i["supplier"],
            "drift_days": drift_days(i),
            "risk_rating": i["risk_rating"],
            "escalation_status": i["escalation_status"],
            "notes": i["notes"],
        }
        for i in items if i["scenario"].startswith("SLIP-")
    ]


def compute_all(items: list[dict]) -> dict:
    return {
        "total_items": len(items),
        "on_time_to_ros": on_time_to_ros(items),
        "forecast_on_time": forecast_on_time(items),
        "drift_by_supplier": drift_by_supplier(items),
        "drift_by_category": drift_by_category(items),
        "drift_by_site": drift_by_site(items),
        "escalation_cycle_time": escalation_cycle_time(items),
        "risk_summary": risk_summary(items),
        "slip_scenarios": slip_scenarios(items),
    }
