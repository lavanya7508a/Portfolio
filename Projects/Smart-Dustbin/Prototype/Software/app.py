"""
Flask Application Backend for Smart Dustbin - AI-Enabled Fill-Level Monitoring System
Field Project: Goundanur, Coimbatore
Author: Lavanya A (25105116 - CSE)
"""

import os
import io
import csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response
from werkzeug.utils import secure_filename

import database as db
import ai_detector

app = Flask(__name__)
app.config["SECRET_KEY"] = "smart-dustbin-goundanur-coimbatore-2026"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "img", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(ai_detector.DETECTIONS_DIR, exist_ok=True)

# Initialize DB on startup if needed
db.init_db()


# --------------------------------------------------------------------------
# Frontend Page Route
# --------------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "templates"), "index.html")


# --------------------------------------------------------------------------
# Dashboard & Bins API
# --------------------------------------------------------------------------
@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    stats = db.get_dashboard_stats()
    return jsonify({"success": True, "stats": stats})


@app.route("/api/bins", methods=["GET"])
def list_bins():
    bins = db.get_all_bins()
    return jsonify({"success": True, "bins": bins})


@app.route("/api/bins/<bin_id>", methods=["GET"])
def get_bin_details(bin_id):
    bin_data = db.get_bin(bin_id)
    if not bin_data:
        return jsonify({"success": False, "error": "Bin not found"}), 404

    # Get recent readings
    conn = db.get_connection()
    readings = conn.execute("""
        SELECT fill_pct, distance_cm, timestamp
        FROM readings
        WHERE bin_id = ?
        ORDER BY timestamp DESC LIMIT 20
    """, (bin_id,)).fetchall()
    conn.close()

    bin_data["readings_history"] = [dict(r) for r in readings]
    return jsonify({"success": True, "bin": bin_data})


@app.route("/api/bins/<bin_id>/reading", methods=["POST"])
def post_bin_reading(bin_id):
    """
    Simulates or receives real ESP32 HC-SR04 ultrasonic sensor telemetry.
    Accepts: { "fill_pct": 85.0 } or { "distance_cm": 15.0 } or { "battery_pct": 92 }
    """
    data = request.get_json() or {}
    fill_pct = data.get("fill_pct")
    distance_cm = data.get("distance_cm")
    battery_pct = data.get("battery_pct")

    # If only distance is provided, calculate fill % (assuming 100cm height bin)
    if fill_pct is None and distance_cm is not None:
        fill_pct = max(0.0, min(100.0, 100.0 - float(distance_cm)))

    if fill_pct is None:
        return jsonify({"success": False, "error": "Must provide fill_pct or distance_cm"}), 400

    updated = db.update_bin_reading(bin_id, fill_pct, distance_cm, battery_pct)
    if not updated:
        return jsonify({"success": False, "error": f"Dustbin {bin_id} not found"}), 404

    return jsonify({
        "success": True,
        "message": f"Telemetry updated for {bin_id}",
        "bin": updated
    })


@app.route("/api/bins/<bin_id>/step", methods=["POST"])
def step_bin_reading(bin_id):
    """Increments or decrements fill percentage by delta."""
    data = request.get_json() or {}
    delta = float(data.get("delta", 10.0))

    b = db.get_bin(bin_id)
    if not b:
        return jsonify({"success": False, "error": "Bin not found"}), 404

    new_pct = max(0.0, min(100.0, b["current_fill_pct"] + delta))
    updated = db.update_bin_reading(bin_id, new_pct)
    return jsonify({"success": True, "bin": updated})


@app.route("/api/bins/<bin_id>/empty", methods=["POST"])
def empty_bin_endpoint(bin_id):
    """Marks bin as emptied / collected. Resets fill level to 0%."""
    data = request.get_json() or {}
    staff_id = data.get("staff_id")
    notes = data.get("notes", "Emptying triggered via dashboard")

    updated = db.empty_bin(bin_id, staff_id=staff_id, notes=notes)
    if not updated:
        return jsonify({"success": False, "error": "Bin not found"}), 404

    return jsonify({
        "success": True,
        "message": f"{bin_id} has been emptied. Level reset to 0%.",
        "bin": updated
    })


# --------------------------------------------------------------------------
# Alerts API
# --------------------------------------------------------------------------
@app.route("/api/alerts", methods=["GET"])
def list_alerts():
    status_filter = request.args.get("status")
    alerts = db.get_alerts(status_filter=status_filter)
    return jsonify({"success": True, "alerts": alerts})


@app.route("/api/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert_endpoint(alert_id):
    resolved = db.resolve_alert(alert_id)
    if not resolved:
        return jsonify({"success": False, "error": "Alert not found"}), 404
    return jsonify({"success": True, "alert": resolved, "message": "Alert marked as resolved"})


@app.route("/api/alerts/simulate-sms", methods=["POST"])
def simulate_sms_alert():
    """Simulates sending an SMS or WhatsApp dispatch alert to sanitation crew."""
    data = request.get_json() or {}
    bin_id = data.get("bin_id", "BIN-001")
    phone = data.get("phone", "+91 98421 54321")
    recipient_name = data.get("staff_name", "Murugan S (Driver)")
    message_text = data.get("message", f"URGENT: Dustbin {bin_id} has reached capacity at Goundanur. Please clear immediately.")

    # Return simulated delivery receipt
    receipt = {
        "gateway": "Coimbatore Smart City SMS Gateway / Twilio Sim",
        "status": "DELIVERED",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipient": f"{recipient_name} ({phone})",
        "message": message_text,
        "simulated": True
    }
    return jsonify({"success": True, "receipt": receipt})


# --------------------------------------------------------------------------
# AI Overflow Detection API
# --------------------------------------------------------------------------
@app.route("/api/ai/detect", methods=["POST"])
def detect_overflow():
    """
    Accepts:
    1. Uploaded image file (multipart/form-data with key 'image')
    OR
    2. Preset sample_id ('clean', 'near_full', 'overflow_spill', 'scattered_litter')
    Optional: mode ('opencv', 'simulated_yolo', 'hybrid')
    Optional: bin_id (e.g. 'BIN-002' to auto-record spillage alert if detected)
    """
    mode = request.form.get("mode", "hybrid")
    sample_id = request.form.get("sample_id")
    bin_id = request.form.get("bin_id")

    image_path = None

    if "image" in request.files and request.files["image"].filename:
        file = request.files["image"]
        filename = secure_filename(file.filename)
        # Unique timestamp prefix
        timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S_")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], timestamp_prefix + filename)
        file.save(save_path)
        image_path = save_path
        original_url = f"/static/img/uploads/{timestamp_prefix + filename}"

    elif sample_id:
        sample_map = {
            "clean": "sample_clean_bin.jpg",
            "near_full": "sample_near_full.jpg",
            "overflow_spill": "sample_overflow_spill.jpg",
            "scattered_litter": "sample_scattered_litter.jpg"
        }
        sample_file = sample_map.get(sample_id, "sample_overflow_spill.jpg")
        image_path = os.path.join(os.path.dirname(__file__), "static", "img", "samples", sample_file)
        original_url = f"/static/img/samples/{sample_file}"

    else:
        return jsonify({"success": False, "error": "Please provide an uploaded image file or a valid sample_id"}), 400

    # Ensure samples exist
    if not os.path.exists(image_path):
        ai_detector.generate_sample_images()

    result = ai_detector.analyze_image(image_path, mode=mode)
    result["original_image_url"] = original_url

    # If overflow or spillage is detected and a bin_id is provided, create an alert
    if result.get("overflow_detected") and bin_id:
        conn = db.get_connection()
        conn.execute("""
            INSERT INTO alerts (bin_id, alert_type, message, status, created_at)
            VALUES (?, 'Spillage Detected', ?, 'Active', ?)
        """, (
            bin_id,
            f"AI Camera detected waste spillage at {bin_id} with {int(result.get('confidence', 0.9)*100)}% confidence.",
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    return jsonify({"success": True, "result": result})


# --------------------------------------------------------------------------
# Collection Management API
# --------------------------------------------------------------------------
@app.route("/api/collections", methods=["GET"])
def list_collections():
    collections = db.get_collections()
    staff = db.get_all_staff()
    return jsonify({
        "success": True,
        "collections": collections,
        "staff": staff
    })


@app.route("/api/collections/create", methods=["POST"])
def create_collection():
    data = request.get_json() or {}
    bin_id = data.get("bin_id")
    staff_id = data.get("staff_id")
    notes = data.get("notes", "Dispatched from dashboard")

    if not bin_id:
        return jsonify({"success": False, "error": "bin_id is required"}), 400

    col = db.dispatch_collection(bin_id, staff_id=staff_id, notes=notes)
    return jsonify({"success": True, "collection": col, "message": "Collection team dispatched"})


@app.route("/api/collections/<int:collection_id>/complete", methods=["POST"])
def complete_collection_endpoint(collection_id):
    data = request.get_json() or {}
    notes = data.get("notes", "Collection confirmed and bin emptied")
    col = db.complete_collection(collection_id, notes=notes)
    if not col:
        return jsonify({"success": False, "error": "Collection record not found"}), 404
    return jsonify({"success": True, "collection": col, "message": "Collection marked completed"})


@app.route("/api/staff", methods=["GET"])
def list_staff():
    staff = db.get_all_staff()
    return jsonify({"success": True, "staff": staff})


# --------------------------------------------------------------------------
# Reports & Analytics API
# --------------------------------------------------------------------------
@app.route("/api/reports/analytics", methods=["GET"])
def report_analytics():
    analytics = db.get_report_analytics()
    return jsonify({"success": True, "analytics": analytics})


@app.route("/api/reports/export-csv", methods=["GET"])
def export_csv_report():
    """Generates a downloadable CSV report of bin telemetry, alerts, and collection performance."""
    conn = db.get_connection()
    bins = conn.execute("SELECT * FROM bins").fetchall()
    collections = conn.execute("SELECT * FROM collections ORDER BY dispatched_at DESC").fetchall()
    conn.close()

    si = io.StringIO()
    cw = csv.writer(si)

    # Header section
    cw.writerow(["SMART DUSTBIN MONITORING SYSTEM - GOUNDANUR COIMBATORE PILOT"])
    cw.writerow(["Generated At", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    cw.writerow(["Presenter", "Lavanya A (25105116 - CSE)"])
    cw.writerow([])

    # Table 1: Bins Status
    cw.writerow(["--- DUSTBIN STATUS SUMMARY ---"])
    cw.writerow(["Bin ID", "Location", "Fill %", "Sensor Distance (cm)", "Status", "Battery %", "Last Updated"])
    for b in bins:
        cw.writerow([b["id"], b["location"], b["current_fill_pct"], b["sensor_distance_cm"], b["status"], b["battery_pct"], b["last_updated"]])

    cw.writerow([])
    # Table 2: Collections History
    cw.writerow(["--- RECENT COLLECTIONS & RESPONSE TIMES ---"])
    cw.writerow(["ID", "Bin ID", "Assigned Staff", "Vehicle ID", "Status", "Dispatched At", "Collected At", "Response Time (min)", "Fill Before %", "Notes"])
    for c in collections:
        cw.writerow([
            c["id"], c["bin_id"], c["staff_name"], c["vehicle_id"], c["status"],
            c["dispatched_at"], c["collected_at"], c["response_time_min"], c["fill_before_pct"], c["notes"]
        ])

    output = io.BytesIO()
    output.write(si.getvalue().encode("utf-8"))
    output.seek(0)

    filename = f"smart_dustbin_report_goundanur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )


# --------------------------------------------------------------------------
# Settings & Hardware Simulation Control API
# --------------------------------------------------------------------------
@app.route("/api/settings", methods=["GET"])
def get_settings():
    settings = db.get_settings()
    return jsonify({"success": True, "settings": settings})


@app.route("/api/settings", methods=["POST"])
def update_settings():
    data = request.get_json() or {}
    for k, v in data.items():
        db.update_setting(k, v)
    return jsonify({"success": True, "settings": db.get_settings()})


@app.route("/api/settings/reset", methods=["POST"])
def reset_database():
    """Resets database and re-seeds Goundanur pilot sample data."""
    db.init_db(force_reset=True)
    ai_detector.generate_sample_images()
    return jsonify({"success": True, "message": "Database and sample data reset to initial pilot state."})


@app.route("/api/simulation/tick", methods=["POST"])
def simulation_tick():
    """
    Advances simulation by adding random waste accumulation to all bins.
    Useful for demonstrating live threshold triggers (e.g. crossing 80%).
    """
    bins = db.get_all_bins()
    updated_bins = []
    import random

    for b in bins:
        # Bins already at 100% don't increase
        if b["current_fill_pct"] < 98:
            increment = random.choice([2.0, 3.5, 5.0, 7.5])
            new_fill = min(100.0, b["current_fill_pct"] + increment)
            u = db.update_bin_reading(b["id"], new_fill)
            updated_bins.append(u)
        else:
            updated_bins.append(b)

    return jsonify({"success": True, "message": "Simulation stepped", "bins": updated_bins})


if __name__ == "__main__":
    ai_detector.generate_sample_images()
    print("=================================================================")
    print(" Smart Dustbin – AI-Enabled Fill-Level Monitoring System")
    print(" Field Pilot: Goundanur, Coimbatore")
    print(" Presenter: Lavanya A (25105116 - CSE)")
    print(" Server running on: http://127.0.0.1:5000")
    print("=================================================================")
    app.run(host="0.0.0.0", port=5000, debug=False)