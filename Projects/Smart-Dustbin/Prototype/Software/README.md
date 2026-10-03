# Smart Dustbin – AI-Enabled Fill-Level Monitoring System

> **A field study on public waste overflow, and a low-cost sensor-based fix that alerts collection teams before a bin overflows.**
> 
> **Presented By:** Lavanya A | Roll: 25105116 | Department of Computer Science & Engineering  
> **Field Site Visited:** Goundanur, Coimbatore  
> **Slogan:** *Clean Environment – Healthy Life | Be smart, use smart dustbins.*

---

## 1. Project Overview & Background

This project addresses severe public waste overflow issues identified during an empirical field visit to **Goundanur, Coimbatore**. Under existing municipal sanitation operations, collection trucks run on a fixed schedule (typically once per day in the early morning), completely blind to real-time waste generation.

As a result, high-density collection points—such as the **Goundanur Main Entrance** and **Goundanur Public Area**—overflow by midday. Waste spills onto surrounding walkways, drawing strays and vermin, emitting foul odors, and exposing residents to health hazards for hours before the next scheduled collection round.

The **Smart Dustbin System** replaces static scheduling with an **IoT-driven demand-response model**:
1. An ultrasonic sensor continuously tracks waste fill height in real time.
2. A warning alert triggers automatically the instant a bin reaches **80% capacity**.
3. A camera and AI-based computer vision model inspect the container rim and surrounding pavement to flag physical waste spillage.
4. Municipal collection teams receive real-time SMS notifications and route dispatch orders via an interactive web dashboard.

---

## 2. Field Study Observations & Problem Statement

### Field Observation Findings (Goundanur, Coimbatore)
- **Midday Overflow:** Bins near the entrance and market areas overflow by 12:00 PM due to peak daytime pedestrian traffic.
- **Fixed Schedule Flaw:** Trucks visit once a day early in the morning before peak waste generation occurs.
- **Average Overflow Exposure:** Bins remain in an overflowing state for an average of **3.2 hours per day**.
- **Pre-collection Overflow Rate:** **68%** of surveyed public dustbins in the locality overflow prior to scheduled truck arrivals.
- **Lack of Segregation:** No on-site wet/dry segregation, causing rapid bin saturation and leachate spillage.

### The Problem Statement (Verbatim)
> *"Public dustbins across our site overflow well before the next scheduled collection — spilling waste onto streets, drawing pests, and putting residents' health at risk, because collection runs on a fixed schedule, not the bin's actual fill level."*

### Root Cause Analysis (5 Whys)
1. **Why do bins overflow before collection?**  
   *Because collection happens only once a day on a fixed schedule.*
2. **Why does collection run on a fixed schedule?**  
   *Because routes are planned without visibility into how quickly each bin fills up.*
3. **Why is there no visibility into fill levels?**  
   *Because municipal staff must physically travel to each bin to check its status.*
4. **Why are bins not monitored remotely?**  
   *Because traditional public bins lack digital telemetry and IoT sensing.*
5. **Root Cause:**  
   *Absence of a real-time fill-level monitoring and proactive alerting feedback loop.*

---

## 3. Project Objectives

1. **Detect Fill Level in Real Time:** Measure distance from bin lid to garbage heap using an HC-SR04 ultrasonic sensor with centimeter precision.
2. **Proactive 80% Alerting:** Automatically dispatch an alert to the collection crew the moment a bin hits 80% capacity, leaving sufficient lead time before overflow occurs.
3. **Cut Overflow Incidents:** Slash public overflow incidents by more than 50% compared to baseline fixed-schedule operations.
4. **Shrink Turnaround Response Time:** Reduce the duration between alert generation and physical truck clearance to **under 2 hours (target < 120 mins)**.
5. **Log Peak-Fill Hours:** Record and visualize hourly fill patterns to enable data-driven dynamic municipal truck routing.
6. **Visual AI Confirmation:** Employ camera-based computer vision and object detection to detect ground litter and overflow spillage that ultrasonic sensors cannot see.

---

## 4. Technology Stack

| Layer | Technologies Used | Description |
|---|---|---|
| **Frontend UI** | React 18, Tailwind CSS, Chart.js, HTML5/CSS3 | Modern green & white responsive single-page application dashboard |
| **Backend API** | Python 3.12, Flask, REST API, Werkzeug | Lightweight, high-performance API server with JSON endpoints |
| **Database** | SQLite 3 | Embedded relational database with ACID compliance for bins, telemetry, alerts & collections |
| **AI / Vision** | OpenCV, NumPy, Pillow, Simulated YOLOv8-Waste | Real contour segmentation, edge density analysis, and dual-mode bounding box detection |
| **IoT / Hardware** | ESP32 (DOIT DEVKIT V1), HC-SR04 Ultrasonic | 2.4 GHz Wi-Fi microcontroller + 40 kHz ultrasonic distance measurement |
| **Testing** | Python `unittest` | Automated test suite verifying APIs, threshold rules, and AI vision pipelines |

---

## 5. System Architecture

```
+-----------------------------------------------------------------------------------+
|                        PHYSICAL IOT HARDWARE / SIMULATOR                          |
|  - HC-SR04 Ultrasonic Sensor in lid (Trig: GPIO 5, Echo: GPIO 18)                 |
|  - ESP32 Microcontroller computes: Fill % = ((100 - Dist) / 100) * 100           |
|  - Wi-Fi / GSM Module (HTTP POST /api/bins/<id>/reading)                          |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ HTTP REST API
+-----------------------------------------------------------------------------------+
|                            FLASK BACKEND & SQLITE                                 |
|  - Ingestion Engine: Validates telemetry & checks threshold rules                 |
|  - Rules Engine:                                                                  |
|      • Fill >= 80%  --> Active Warning Alert + Simulated SMS Notification         |
|      • Fill >= 95%  --> Critical Overflow Alert                                   |
|      • Emptied = 0% --> Auto-resolves alerts & logs turnaround response time      |
|  - AI Vision Engine: Dual-mode OpenCV contour density & YOLOv8 bounding boxes     |
|  - SQLite Storage: `smart_dustbin.db` (bins, readings, alerts, staff, collections)|
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ JSON API (Polling / SSE)
+-----------------------------------------------------------------------------------+
|                     REACT 18 RESPONSIVE WEB DASHBOARD                             |
|  - Green & White theme matching Coimbatore Clean Environment campaign             |
|  - 8 Comprehensive Modules:                                                       |
|      1. Demo Login (Supervisor / Staff / Admin)                                   |
|      2. Dashboard (KPIs, Live Gauges, Chart.js Midday Peak Curve, Alerts)         |
|      3. Dustbin Monitoring (Goundanur Entrance, Public Area, Street 1 & 2)        |
|      4. AI Overflow Detection (Upload, 4 Presets, Bounding Boxes, Confidence)     |
|      5. Alert Center (80% Warning, Spillage, Resolve, Simulated SMS Gateway)      |
|      6. Collection Management (Staff Roster, Dispatch Queue, Mark Collected)      |
|      7. Reports & Analytics (Field Stats, Response Times, Download CSV & PDF)     |
|      8. Hardware Bench & Settings (Interactive Slider, Audio Alarm, DB Reset)     |
+-----------------------------------------------------------------------------------+
```

---

## 6. Detailed Application Modules

### 1. Dashboard
- **5 High-Level KPI Cards:** Total Bins, Normal (<80%), Warning (≥80%), Critical Overflow (≥95%), and Site-Wide Average Fill Level.
- **Hourly Fill Trend Chart:** Interactive Chart.js graph illustrating the 12:00 PM midday accumulation surge observed at Goundanur.
- **Live Dustbin Cards:** Real-time vertical liquid gauges displaying fill level, ultrasonic distance in cm, battery health, and quick action controls.
- **Active Alerts Drawer:** Shows urgent alerts with 1-click SMS simulation to dispatch drivers.

### 2. Dustbin Monitoring
Dedicated telemetry cards for all 4 pilot locations:
- **`BIN-001`**: Goundanur Main Entrance (High traffic entrance)
- **`BIN-002`**: Goundanur Public Area (Market/gathering zone)
- **`BIN-003`**: Goundanur Street 1 (Residential lane)
- **`BIN-004`**: Goundanur Street 2 (Commercial shops)
Includes quick-action buttons on every card: `+10%`, `-10%`, `85% Warning`, `98% Overflow`, and `Empty Bin`.

### 3. AI Overflow & Spillage Detection
- **Dual Mode AI Engine:**
  - **Real OpenCV Analysis:** Calculates pixel edge density and contour distributions in the bin rim zone (overflow) and pavement zone (spillage).
  - **Simulated Deep Learning (YOLOv8-Waste):** Simulates fine-tuned object detection with color-coded bounding boxes, confidence ratings (85%–96%), and classified labels (`Overflow Waste Cluster`, `Ground Spillage / Litter`, `Bin Structure`).
- **1-Click Test Samples:** Built-in test buttons for Clean Bin, Near Full (80%), Severe Overflow & Spillage, and Scattered Litter.
- **Custom Upload Support:** Allows users to upload their own field photos.
- **Direct Dispatch Trigger:** One-click button to immediately dispatch a sanitation crew when spillage is confirmed.

### 4. Alert Management
- **Threshold Rules:** Automatically triggers `Warning 80%` when level reaches 80.0%, and upgrades to `Critical Overflow` at 95.0%.
- **SMS / WhatsApp Simulation Modal:** Previews the exact SMS transmission receipt sent to the assigned sanitation crew (+91 98421 54321).
- **Resolve Workflow:** Allows municipal supervisors to manually or automatically resolve alerts once cleared.

### 5. Collection Management
- **Crew Roster:** Displays active drivers, supervisors, and assigned compaction vehicles (e.g. `TN-37-CZ-4102`).
- **Dispatch Queue:** Assigns available drivers to pending bin pickups.
- **Mark as Collected:** Automatically resets bin fill level to 0%, calculates turnaround response time in minutes, and logs historical records.

### 6. Analytics & Reports
- **Impact Comparison:** Highlights the 3.2 hrs/day baseline overflow duration vs. the 52-minute smart turnaround time.
- **Scorecard Table:** Bin-by-bin performance history.
- **One-Click CSV Export:** Generates and downloads a clean `.csv` spreadsheet of all telemetry and collection records.
- **Print / PDF Report:** Formatted for academic report submission.

### 7. Hardware Bench & Settings
- **Virtual ESP32 Bench:** Live interactive slider allowing examiners to test ultrasonic distance calculations and threshold alerts in real time.
- **Audio Chime Toggle:** Uses the Web Audio API to generate a clean warning chime whenever a bin crosses 80%.
- **Database Reset:** 1-click button to reset the database and re-seed the original Goundanur field pilot state.

### 8. Demo Authentication
- Multi-role switch: Municipal Supervisor (Lavanya A), Collection Driver (Murugan S), and Route Inspector (Priya K).

---

## 7. Installation & How to Run

### Prerequisites
- Windows 10/11, macOS, or Linux
- Python 3.10 or higher (Python 3.12 recommended)

### Quick Start (Windows)
Simply double-click:
```cmd
run.bat
```
This batch script detects Python, starts the Flask server on `http://127.0.0.1:5000`, and opens the dashboard in your default browser.

### Manual Start (Command Line)
1. Open terminal and navigate to the project directory:
   ```bash
   cd "C:\Users\user\.gemini\antigravity\scratch\smart-dustbin-monitor"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 8. Running the ESP32 Hardware Simulator

To simulate live telemetry packets sent over the network by a physical ESP32 node:
```bash
# Continuous simulation loop:
python esp32_simulator.py --bin BIN-001 --continuous --interval 3

# One-off telemetry burst across all 4 bins:
python esp32_simulator.py

# Manually set a bin to 85% to trigger a live warning:
python esp32_simulator.py --bin BIN-003 --fill 85
```

---

## 9. Running Automated Tests

Run the included test suite to verify database integrity, API routes, threshold triggers, and AI detection:
```bash
python -m unittest tests/test_api.py
```
Expected output:
```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.31s

OK
```

---

## 10. Physical ESP32 Hardware Deployment

For physical demonstrations with real hardware, the complete Arduino C++ firmware is provided in:
[`firmware/esp32_firmware.ino`](firmware/esp32_firmware.ino)

### Circuit Wiring Reference
| HC-SR04 Sensor Pin | ESP32 Pin | Note |
|---|---|---|
| **VCC** | 5V / VIN | Power supply |
| **GND** | GND | Ground |
| **TRIG** | GPIO 5 | Digital Output (10µs pulse) |
| **ECHO** | GPIO 18 | Digital Input (via 1kΩ / 2kΩ voltage divider to step 5V down to 3.3V) |
| **LED Warning** | GPIO 2 | On-board LED indicator for ≥ 80% threshold |
| **Buzzer (Optional)** | GPIO 4 | Local audible alert |

---

## 11. AI Usage Declaration

As presented in **Slide 10** of the original project submission:
> *"AI assistance was used for research support, system modeling, edge-detection pipeline prototyping, and UI dashboard visualization. All algorithms, database schemas, threshold calculations, and field findings were reviewed, fact-checked, verified, and adapted for the Goundanur municipal context."*
