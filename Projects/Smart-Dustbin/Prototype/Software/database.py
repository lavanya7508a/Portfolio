"""
Database module for Smart Dustbin - AI-Enabled Fill-Level Monitoring System
Field Site: Goundanur, Coimbatore
Project Author: Lavanya A (25105116 - CSE)
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "smart_dustbin.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(force_reset=False):
    """Creates tables and populates realistic initial seed data for Goundanur pilot."""
    if force_reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    cur = conn.cursor()

    # Bins table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bins (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        height_cm REAL DEFAULT 100.0,
        current_fill_pct REAL DEFAULT 0.0,
        sensor_distance_cm REAL DEFAULT 100.0,
        status TEXT DEFAULT 'Normal',
        battery_pct INTEGER DEFAULT 95,
        last_updated TEXT
    )
    """)

    # Telemetry readings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bin_id TEXT NOT NULL,
        fill_pct REAL NOT NULL,
        distance_cm REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (bin_id) REFERENCES bins (id) ON DELETE CASCADE
    )
    """)

    # Alerts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bin_id TEXT NOT NULL,
        alert_type TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        created_at TEXT NOT NULL,
        resolved_at TEXT,
        FOREIGN KEY (bin_id) REFERENCES bins (id) ON DELETE CASCADE
    )
    """)

    # Staff table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        role TEXT NOT NULL,
        vehicle_id TEXT NOT NULL,
        status TEXT DEFAULT 'Available'
    )
    """)

    # Collections table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bin_id TEXT NOT NULL,
        staff_id INTEGER,
        staff_name TEXT,
        vehicle_id TEXT,
        status TEXT DEFAULT 'Pending',
        dispatched_at TEXT NOT NULL,
        collected_at TEXT,
        response_time_min INTEGER,
        fill_before_pct REAL,
        fill_after_pct REAL,
        notes TEXT,
        FOREIGN KEY (bin_id) REFERENCES bins (id) ON DELETE CASCADE,
        FOREIGN KEY (staff_id) REFERENCES staff (id)
    )
    """)

    # Settings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    conn.commit()

    # Check if data already seeded
    cur.execute("SELECT COUNT(*) AS count FROM bins")
    if cur.fetchone()["count"] == 0:
        _seed_demo_data(conn)

    conn.close()


def _seed_demo_data(conn):
    """Seed initial demo data reflecting the Goundanur, Coimbatore field study."""
    cur = conn.cursor()
    now = datetime.now()

    # 1. Bins (HC-SR04 ultrasonic simulation: 100cm height bin)
    # Fill % = (100 - distance_cm) / 100 * 100
    bins_data = [
        ("BIN-001", "Goundanur Main Entrance Bin", "Goundanur Main Entrance", 10.9824, 76.9631, 100.0, 85.0, 15.0, "Warning", 92, (now - timedelta(minutes=2)).isoformat()),
        ("BIN-002", "Goundanur Public Area Bin", "Goundanur Public Area", 10.9839, 76.9645, 100.0, 95.0, 5.0, "Overflow", 88, (now - timedelta(minutes=5)).isoformat()),
        ("BIN-003", "Goundanur Street 1 Bin", "Goundanur Street 1", 10.9815, 76.9618, 100.0, 45.0, 55.0, "Normal", 98, (now - timedelta(minutes=10)).isoformat()),
        ("BIN-004", "Goundanur Street 2 Bin", "Goundanur Street 2", 10.9842, 76.9660, 100.0, 70.0, 30.0, "Normal", 91, (now - timedelta(minutes=7)).isoformat()),
    ]
    cur.executemany("""
    INSERT INTO bins (id, name, location, latitude, longitude, height_cm, current_fill_pct, sensor_distance_cm, status, battery_pct, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, bins_data)

    # 2. Staff
    staff_data = [
        ("Murugan S", "+91 98421 54321", "Driver", "TN-37-CZ-4102", "Available"),
        ("Priya K", "+91 94432 67890", "Route Supervisor", "TN-37-CZ-4102", "Available"),
        ("Ramesh M", "+91 97865 12345", "Field Operator", "TN-37-CZ-1099", "On Route"),
        ("Kavitha R", "+91 98940 33211", "Field Operator", "TN-37-CZ-1099", "Available"),
    ]
    cur.executemany("""
    INSERT INTO staff (name, phone, role, vehicle_id, status)
    VALUES (?, ?, ?, ?, ?)
    """, staff_data)

    # 3. Settings
    settings_data = [
        ("warning_threshold", "80"),
        ("critical_threshold", "95"),
        ("auto_simulation_enabled", "false"),
        ("simulation_speed", "1"),
        ("sound_alerts_enabled", "true"),
        ("sms_gateway_simulation", "enabled"),
    ]
    cur.executemany("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", settings_data)

    # 4. Realistic Readings History (hourly intervals for the last 12 hours)
    historical_readings = []
    # Morning to afternoon buildup demonstrating midday peak overflow found during Goundanur field observation
    curve_data = [
        # (hours_ago, bin1_pct, bin2_pct, bin3_pct, bin4_pct)
        (12, 18, 22, 10, 15),
        (10, 28, 35, 15, 25),
        (8,  42, 54, 20, 38),
        (6,  60, 72, 28, 50),
        (4,  78, 86, 35, 60),
        (2,  84, 93, 40, 68),
        (0,  85, 95, 45, 70),
    ]
    for h_ago, b1, b2, b3, b4 in curve_data:
        t_str = (now - timedelta(hours=h_ago)).isoformat()
        historical_readings.append(("BIN-001", b1, 100.0 - b1, t_str))
        historical_readings.append(("BIN-002", b2, 100.0 - b2, t_str))
        historical_readings.append(("BIN-003", b3, 100.0 - b3, t_str))
        historical_readings.append(("BIN-004", b4, 100.0 - b4, t_str))

    cur.executemany("""
    INSERT INTO readings (bin_id, fill_pct, distance_cm, timestamp)
    VALUES (?, ?, ?, ?)
    """, historical_readings)

    # 5. Alerts
    alerts_data = [
        ("BIN-002", "Critical Overflow", "Bin exceeded 95% capacity at Goundanur Public Area. Risk of spillage.", "Active", (now - timedelta(minutes=45)).isoformat(), None),
        ("BIN-001", "Warning 80%", "Bin reached 85% capacity at Goundanur Main Entrance. Needs collection.", "Active", (now - timedelta(minutes=25)).isoformat(), None),
        ("BIN-004", "Warning 80%", "Bin reached 82% threshold earlier today.", "Resolved", (now - timedelta(hours=5)).isoformat(), (now - timedelta(hours=3, minutes=45)).isoformat()),
        ("BIN-002", "Spillage Detected", "AI camera flagged litter scattered outside bin rim.", "Resolved", (now - timedelta(hours=8)).isoformat(), (now - timedelta(hours=7)).isoformat()),
    ]
    cur.executemany("""
    INSERT INTO alerts (bin_id, alert_type, message, status, created_at, resolved_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, alerts_data)

    # 6. Collections
    collections_data = [
        ("BIN-002", 3, "Ramesh M", "TN-37-CZ-1099", "Dispatched", (now - timedelta(minutes=20)).isoformat(), None, None, 95.0, None, "Immediate dispatch for public area overflow."),
        ("BIN-004", 1, "Murugan S", "TN-37-CZ-4102", "Completed", (now - timedelta(hours=5)).isoformat(), (now - timedelta(hours=4, minutes=12)).isoformat(), 48, 88.0, 0.0, "Routine morning clearance completed."),
        ("BIN-001", 1, "Murugan S", "TN-37-CZ-4102", "Completed", (now - timedelta(hours=9)).isoformat(), (now - timedelta(hours=7, minutes=55)).isoformat(), 65, 82.0, 0.0, "Cleared early morning overflow."),
        ("BIN-003", 3, "Ramesh M", "TN-37-CZ-1099", "Completed", (now - timedelta(hours=24)).isoformat(), (now - timedelta(hours=23, minutes=10)).isoformat(), 50, 78.0, 0.0, "Yesterday regular residential pickup."),
    ]
    cur.executemany("""
    INSERT INTO collections (bin_id, staff_id, staff_name, vehicle_id, status, dispatched_at, collected_at, response_time_min, fill_before_pct, fill_after_pct, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, collections_data)

    conn.commit()


# =========================================================================
# Query & Mutation Helpers
# =========================================================================

def get_all_bins():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bins ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_bin(bin_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_bin_reading(bin_id, fill_pct, distance_cm=None, battery_pct=None):
    """
    Updates the fill level of a dustbin, calculates status, creates alerts when hitting thresholds.
    Threshold logic:
      - >= 95% -> 'Overflow' (Critical alert)
      - >= 80% -> 'Warning' (Warning alert)
      - < 80%  -> 'Normal'
    """
    conn = get_connection()
    cur = conn.cursor()

    bin_row = cur.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    if not bin_row:
        conn.close()
        return None

    height_cm = bin_row["height_cm"]
    fill_pct = max(0.0, min(100.0, float(fill_pct)))

    if distance_cm is None:
        # Calculate ultrasonic distance based on height and fill %
        distance_cm = round(height_cm * (1.0 - (fill_pct / 100.0)), 1)
    else:
        distance_cm = max(0.0, float(distance_cm))

    # Determine status
    if fill_pct >= 95.0:
        status = "Overflow"
    elif fill_pct >= 80.0:
        status = "Warning"
    else:
        status = "Normal"

    now_iso = datetime.now().isoformat()
    battery = battery_pct if battery_pct is not None else bin_row["battery_pct"]

    cur.execute("""
    UPDATE bins
    SET current_fill_pct = ?, sensor_distance_cm = ?, status = ?, battery_pct = ?, last_updated = ?
    WHERE id = ?
    """, (fill_pct, distance_cm, status, battery, now_iso, bin_id))

    # Log reading
    cur.execute("""
    INSERT INTO readings (bin_id, fill_pct, distance_cm, timestamp)
    VALUES (?, ?, ?, ?)
    """, (bin_id, fill_pct, distance_cm, now_iso))

    # Check alert triggering
    if status in ("Warning", "Overflow"):
        # Check if an active alert for this bin already exists
        existing_alert = cur.execute("""
        SELECT id, alert_type FROM alerts
        WHERE bin_id = ? AND status = 'Active'
        """, (bin_id,)).fetchone()

        alert_type = "Critical Overflow" if status == "Overflow" else "Warning 80%"
        alert_msg = f"{bin_row['name']} has reached {fill_pct:.1f}% capacity at {bin_row['location']}."

        if not existing_alert:
            cur.execute("""
            INSERT INTO alerts (bin_id, alert_type, message, status, created_at)
            VALUES (?, ?, ?, 'Active', ?)
            """, (bin_id, alert_type, alert_msg, now_iso))
        elif status == "Overflow" and existing_alert["alert_type"] != "Critical Overflow":
            # Upgrade warning to critical overflow
            cur.execute("""
            UPDATE alerts
            SET alert_type = ?, message = ?, created_at = ?
            WHERE id = ?
            """, (alert_type, alert_msg, now_iso, existing_alert["id"]))
    elif status == "Normal":
        # If bin was previously cleared below 80%, auto-resolve active alerts
        cur.execute("""
        UPDATE alerts
        SET status = 'Resolved', resolved_at = ?
        WHERE bin_id = ? AND status = 'Active'
        """, (now_iso, bin_id))

    conn.commit()

    updated = cur.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    conn.close()
    return dict(updated)


def empty_bin(bin_id, staff_id=None, notes="Manual or IoT emptying trigger"):
    """
    Simulates waste collection: resets fill level to 0%, sensor distance to 100cm,
    marks any active collection as Completed, and resolves active alerts.
    """
    conn = get_connection()
    cur = conn.cursor()

    bin_row = cur.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    if not bin_row:
        conn.close()
        return None

    fill_before = bin_row["current_fill_pct"]
    now_iso = datetime.now().isoformat()

    # Reset bin
    cur.execute("""
    UPDATE bins
    SET current_fill_pct = 0.0, sensor_distance_cm = height_cm, status = 'Normal', last_updated = ?
    WHERE id = ?
    """, (now_iso, bin_id))

    # Log reading
    cur.execute("""
    INSERT INTO readings (bin_id, fill_pct, distance_cm, timestamp)
    VALUES (?, 0.0, ?, ?)
    """, (bin_id, bin_row["height_cm"], now_iso))

    # Auto-resolve active alerts
    cur.execute("""
    UPDATE alerts
    SET status = 'Resolved', resolved_at = ?
    WHERE bin_id = ? AND status = 'Active'
    """, (now_iso, bin_id))

    # Check if there is a pending or dispatched collection for this bin
    pending_col = cur.execute("""
    SELECT * FROM collections
    WHERE bin_id = ? AND status IN ('Pending', 'Dispatched')
    ORDER BY id DESC LIMIT 1
    """, (bin_id,)).fetchone()

    if pending_col:
        disp_time = datetime.fromisoformat(pending_col["dispatched_at"])
        resp_min = max(1, int((datetime.now() - disp_time).total_seconds() // 60))
        cur.execute("""
        UPDATE collections
        SET status = 'Completed', collected_at = ?, response_time_min = ?, fill_after_pct = 0.0, notes = ?
        WHERE id = ?
        """, (now_iso, resp_min, notes, pending_col["id"]))
    else:
        # Create a completed collection record
        staff_row = None
        if staff_id:
            staff_row = cur.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
        if not staff_row:
            staff_row = cur.execute("SELECT * FROM staff LIMIT 1").fetchone()

        cur.execute("""
        INSERT INTO collections (bin_id, staff_id, staff_name, vehicle_id, status, dispatched_at, collected_at, response_time_min, fill_before_pct, fill_after_pct, notes)
        VALUES (?, ?, ?, ?, 'Completed', ?, ?, 35, ?, 0.0, ?)
        """, (
            bin_id,
            staff_row["id"] if staff_row else 1,
            staff_row["name"] if staff_row else "Murugan S",
            staff_row["vehicle_id"] if staff_row else "TN-37-CZ-4102",
            (datetime.now() - timedelta(minutes=35)).isoformat(),
            now_iso,
            fill_before,
            notes
        ))

    conn.commit()
    updated = cur.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    conn.close()
    return dict(updated)


def get_alerts(status_filter=None, limit=50):
    conn = get_connection()
    query = """
    SELECT a.*, b.name as bin_name, b.location as bin_location
    FROM alerts a
    LEFT JOIN bins b ON a.bin_id = b.id
    """
    params = []
    if status_filter:
        query += " WHERE a.status = ?"
        params.append(status_filter)
    query += " ORDER BY a.created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def resolve_alert(alert_id):
    conn = get_connection()
    now_iso = datetime.now().isoformat()
    conn.execute("""
    UPDATE alerts
    SET status = 'Resolved', resolved_at = ?
    WHERE id = ?
    """, (now_iso, alert_id))
    conn.commit()
    row = conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_collections(limit=50):
    conn = get_connection()
    rows = conn.execute("""
    SELECT c.*, b.name as bin_name, b.location as bin_location
    FROM collections c
    LEFT JOIN bins b ON c.bin_id = b.id
    ORDER BY c.dispatched_at DESC
    LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def dispatch_collection(bin_id, staff_id=None, notes="Dispatched via dashboard alert"):
    conn = get_connection()
    cur = conn.cursor()

    # Get staff info
    if staff_id:
        staff_row = cur.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
    else:
        staff_row = cur.execute("SELECT * FROM staff WHERE status = 'Available' LIMIT 1").fetchone()
        if not staff_row:
            staff_row = cur.execute("SELECT * FROM staff LIMIT 1").fetchone()

    bin_row = cur.execute("SELECT * FROM bins WHERE id = ?", (bin_id,)).fetchone()
    now_iso = datetime.now().isoformat()

    cur.execute("""
    INSERT INTO collections (bin_id, staff_id, staff_name, vehicle_id, status, dispatched_at, fill_before_pct, notes)
    VALUES (?, ?, ?, ?, 'Dispatched', ?, ?, ?)
    """, (
        bin_id,
        staff_row["id"] if staff_row else None,
        staff_row["name"] if staff_row else "Sanitation Team",
        staff_row["vehicle_id"] if staff_row else "TN-37-CZ-4102",
        now_iso,
        bin_row["current_fill_pct"] if bin_row else 85.0,
        notes
    ))

    if staff_row:
        cur.execute("UPDATE staff SET status = 'On Route' WHERE id = ?", (staff_row["id"],))

    conn.commit()
    col_id = cur.lastrowid
    row = cur.execute("SELECT * FROM collections WHERE id = ?", (col_id,)).fetchone()
    conn.close()
    return dict(row)


def complete_collection(collection_id, notes="Collection verified and bin cleared"):
    conn = get_connection()
    cur = conn.cursor()
    col_row = cur.execute("SELECT * FROM collections WHERE id = ?", (collection_id,)).fetchone()
    if not col_row:
        conn.close()
        return None

    now = datetime.now()
    now_iso = now.isoformat()
    disp_time = datetime.fromisoformat(col_row["dispatched_at"])
    resp_min = max(1, int((now - disp_time).total_seconds() // 60))

    cur.execute("""
    UPDATE collections
    SET status = 'Completed', collected_at = ?, response_time_min = ?, fill_after_pct = 0.0, notes = ?
    WHERE id = ?
    """, (now_iso, resp_min, notes, collection_id))

    # Reset bin fill level to 0
    cur.execute("""
    UPDATE bins
    SET current_fill_pct = 0.0, sensor_distance_cm = height_cm, status = 'Normal', last_updated = ?
    WHERE id = ?
    """, (now_iso, col_row["bin_id"]))

    # Free staff
    if col_row["staff_id"]:
        cur.execute("UPDATE staff SET status = 'Available' WHERE id = ?", (col_row["staff_id"],))

    # Resolve active alerts for this bin
    cur.execute("""
    UPDATE alerts
    SET status = 'Resolved', resolved_at = ?
    WHERE bin_id = ? AND status = 'Active'
    """, (now_iso, col_row["bin_id"]))

    conn.commit()
    row = cur.execute("SELECT * FROM collections WHERE id = ?", (collection_id,)).fetchone()
    conn.close()
    return dict(row)


def get_all_staff():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM staff ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_stats():
    conn = get_connection()
    bins = conn.execute("SELECT * FROM bins").fetchall()
    total_bins = len(bins)
    normal_bins = sum(1 for b in bins if b["status"] == "Normal")
    warning_bins = sum(1 for b in bins if b["status"] == "Warning")
    overflow_bins = sum(1 for b in bins if b["status"] == "Overflow")
    avg_fill = round(sum(b["current_fill_pct"] for b in bins) / total_bins, 1) if total_bins > 0 else 0

    active_alerts_count = conn.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Active'").fetchone()[0]
    pending_collections_count = conn.execute("SELECT COUNT(*) FROM collections WHERE status IN ('Pending', 'Dispatched')").fetchone()[0]

    # Average response time in minutes
    resp_row = conn.execute("SELECT AVG(response_time_min) FROM collections WHERE status = 'Completed' AND response_time_min IS NOT NULL").fetchone()[0]
    avg_response_time = round(resp_row, 1) if resp_row else 52.0

    conn.close()
    return {
        "total_bins": total_bins,
        "normal_bins": normal_bins,
        "warning_bins": warning_bins,
        "overflow_bins": overflow_bins,
        "average_fill_level": avg_fill,
        "active_alerts_count": active_alerts_count,
        "pending_collections_count": pending_collections_count,
        "avg_response_time_min": avg_response_time,
    }


def get_report_analytics():
    conn = get_connection()
    bins = conn.execute("SELECT * FROM bins").fetchall()
    alerts = conn.execute("SELECT * FROM alerts ORDER BY created_at DESC").fetchall()
    collections = conn.execute("SELECT * FROM collections ORDER BY dispatched_at DESC").fetchall()

    # Peak fill hours (sample aggregated by 2-hour windows)
    hourly_distribution = [
        {"time": "06:00 AM", "fill_avg": 22, "overflow_risk": "Low"},
        {"time": "08:00 AM", "fill_avg": 38, "overflow_risk": "Low"},
        {"time": "10:00 AM", "fill_avg": 58, "overflow_risk": "Medium"},
        {"time": "12:00 PM (Midday)", "fill_avg": 84, "overflow_risk": "High - Peak Demand"},
        {"time": "02:00 PM", "fill_avg": 92, "overflow_risk": "Critical Overflow"},
        {"time": "04:00 PM", "fill_avg": 76, "overflow_risk": "High"},
        {"time": "06:00 PM", "fill_avg": 68, "overflow_risk": "Medium"},
        {"time": "08:00 PM", "fill_avg": 45, "overflow_risk": "Low"},
    ]

    bin_summaries = []
    for b in bins:
        b_alerts = [a for a in alerts if a["bin_id"] == b["id"]]
        b_cols = [c for c in collections if c["bin_id"] == b["id"] and c["status"] == "Completed"]
        bin_summaries.append({
            "id": b["id"],
            "name": b["name"],
            "location": b["location"],
            "current_fill": b["current_fill_pct"],
            "status": b["status"],
            "alert_count": len(b_alerts),
            "collection_count": len(b_cols),
            "battery": b["battery_pct"],
        })

    conn.close()
    return {
        "hourly_distribution": hourly_distribution,
        "bin_summaries": bin_summaries,
        "field_stats": {
            "avg_overflow_duration_hrs": 3.2,
            "precollection_overflow_pct": 68,
            "target_response_time_min": 120,
            "actual_avg_response_time_min": 52,
            "site": "Goundanur, Coimbatore",
            "presenter": "Lavanya A (25105116 - CSE)",
        }
    }


def get_settings():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM settings").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}


def update_setting(key, value):
    conn = get_connection()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db(force_reset=True)
    print("Smart Dustbin SQLite Database initialized with Goundanur pilot seed data.")