"""Tests for OFE KPI computation against the simulated dataset.

Dataset facts the tests pin down (change the data, update these on purpose):
  - 40 line items, 20 per site (HELIOS-ALPHA / HELIOS-BETA)
  - 9 equipment categories covering the JD list
  - exactly 3 slip scenarios: factory delay, FAT fail, logistics delay
  - 29 delivered items
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ofe_kpi import (  # noqa: E402
    compute_all, drift_by_category, drift_by_supplier, drift_days,
    escalation_cycle_time, load_items, on_time_to_ros, slip_scenarios,
)

ITEMS = load_items(ROOT / "data" / "ofe_line_items.csv")
BY_ID = {i["line_item_id"]: i for i in ITEMS}

JD_CATEGORIES = {
    "Switchgear", "Transformers", "UPS", "Generators", "Busway",
    "PDUs", "Chillers", "CDUs", "Air Handlers",
}


def test_dataset_shape():
    assert len(ITEMS) == 40
    sites = {i["site"] for i in ITEMS}
    assert sites == {"HELIOS-ALPHA", "HELIOS-BETA"}
    for site in sites:
        assert sum(1 for i in ITEMS if i["site"] == site) == 20


def test_categories_cover_jd_list():
    assert {i["equipment_category"] for i in ITEMS} == JD_CATEGORIES


def test_required_fields_present():
    required = [
        "site", "equipment_category", "supplier", "po_date",
        "submittal_status", "production_slot_start", "production_slot_end",
        "fat_date", "fat_result", "ship_date", "ros_date_planned",
        "ros_date_forecast", "risk_rating", "escalation_status",
    ]
    for item in ITEMS:
        for field in required:
            assert field in item, (item["line_item_id"], field)
        assert item["ros_date_planned"] is not None
        assert item["ros_date_forecast"] is not None


def test_three_slip_scenarios():
    slips = slip_scenarios(ITEMS)
    assert len(slips) == 3
    assert {s["scenario"] for s in slips} == {
        "SLIP-FACTORY-DELAY", "SLIP-FAT-FAIL", "SLIP-LOGISTICS"}
    # Each slip is a real schedule problem, not a label on an on-time item.
    for s in slips:
        assert s["drift_days"] > 0
        assert s["risk_rating"] == "High"
        assert s["escalation_status"] == "Open"


def test_slip_drift_values():
    assert drift_days(BY_ID["OFE-003"]) == 35   # factory delay, transformer
    assert drift_days(BY_ID["OFE-010"]) == 28   # FAT fail, CDU
    assert drift_days(BY_ID["OFE-025"]) == 28   # logistics delay, chiller


def test_on_time_to_ros():
    result = on_time_to_ros(ITEMS)
    assert result["delivered"] == 29
    # Hand-counted from the dataset: delivered items with actual ROS <= plan.
    late_delivered = [
        i["line_item_id"] for i in ITEMS
        if i["ros_date_actual"] is not None
        and i["ros_date_actual"] > i["ros_date_planned"]
    ]
    assert result["on_time"] == 29 - len(late_delivered)
    assert 0.0 < result["rate"] < 1.0


def test_drift_groupings_are_consistent():
    for groups in (drift_by_supplier(ITEMS), drift_by_category(ITEMS)):
        assert sum(g["count"] for g in groups.values()) == 40
    cat = drift_by_category(ITEMS)
    # Transformers carry the factory-delay slip, CDUs the FAT fail.
    assert cat["Transformers"]["max_drift_days"] == 35
    assert cat["CDUs"]["max_drift_days"] == 28
    sup = drift_by_supplier(ITEMS)
    assert sup["ABB"]["max_drift_days"] == 35


def test_escalation_cycle_time():
    result = escalation_cycle_time(ITEMS)
    assert result["closed_count"] == 6
    assert result["open_items"] == ["OFE-003", "OFE-010", "OFE-025"]
    for c in result["closed"]:
        assert c["cycle_days"] > 0
    assert result["mean_cycle_days"] > 0


def test_fat_fail_item_has_no_ship_date():
    fat_fail = BY_ID["OFE-010"]
    assert fat_fail["fat_result"] == "Fail"
    # A unit that failed FAT has not shipped; the tracker must show that.
    assert fat_fail["ship_date"] is None
    assert fat_fail["ros_date_actual"] is None


def test_compute_all_keys():
    k = compute_all(ITEMS)
    for key in ("total_items", "on_time_to_ros", "forecast_on_time",
                "drift_by_supplier", "drift_by_category", "drift_by_site",
                "escalation_cycle_time", "risk_summary", "slip_scenarios"):
        assert key in k
    assert k["risk_summary"]["open_high_risk"] == ["OFE-003", "OFE-010", "OFE-025"]
