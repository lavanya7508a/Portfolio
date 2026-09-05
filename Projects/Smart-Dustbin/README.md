# Smart Dustbin

## AI-Enabled Fill-Level Monitoring System

A smart waste-management solution designed to monitor dustbin fill levels in real time and alert collection teams before the bin overflows.

## Problem Statement

During the field visit, overflowing public dustbins were observed before the next scheduled collection. The fixed collection schedule does not consider the actual fill level of individual bins, resulting in waste overflow and poor waste-management conditions.

## Field Study

- **Location:** Goundanur, Coimbatore
- Bins were observed overflowing by midday near the entrance.
- No wet/dry waste segregation was observed at the site.
- Collection was carried out once a day before peak demand.

## Objectives

- Detect the bin fill level in real time.
- Alert collection staff when the bin reaches 80% capacity.
- Reduce waste overflow incidents.
- Reduce the response time between an alert and waste collection.
- Record fill-level data to identify peak filling periods.

## Proposed Solution

The Smart Dustbin combines ultrasonic sensing with vision-based overflow detection.

The ultrasonic sensor continuously monitors the distance between the sensor and the waste and converts the reading into a fill percentage.

A camera with an object-detection model can visually confirm overflow and spillage around the bin.

When the fill level reaches the defined threshold, the system sends an alert to the collection team through Wi-Fi or GSM.

## System Architecture

1. Ultrasonic sensor measures the waste level.
2. ESP32/microcontroller processes the sensor reading.
3. Fill percentage is calculated.
4. Wi-Fi/GSM sends an alert when the threshold is reached.
5. Dashboard/SMS notifies the collection staff.
6. After the bin is emptied, monitoring automatically continues.

## Hardware Components

- ESP32
- Ultrasonic Sensor
- Camera
- Wi-Fi/GSM Module
- Smart Dustbin

## AI / Sensing Technology

- Ultrasonic sensor for continuous fill-level monitoring.
- Camera-based object detection for overflow and spillage verification.
- Labelled images can be used to train the object-detection model.

## Key Features

- Real-time fill-level monitoring
- 80% fill-level alert
- Overflow detection
- Wi-Fi/GSM notification
- Dashboard monitoring
- Continuous data logging
- Low-cost hardware approach

## Expected Outcomes

| Area | Existing System | Smart Dustbin |
|---|---|---|
| Collection Trigger | Fixed schedule | Actual fill level |
| Overflow | Frequent and unpredictable | Targeted reduction |
| Response Time | Same day or later | Target: under 2 hours |
| Visibility | No live information | Continuous fill-level data |

## Benefits

- Helps prevent overflowing dustbins.
- Enables demand-based waste collection.
- Reduces unnecessary collection trips.
- Provides real-time information to collection teams.
- Supports cleaner and healthier public spaces.

## Tools & Technologies

- Arduino / ESP32
- Ultrasonic Sensor
- Camera
- Wi-Fi / GSM
- Object Detection
- AI-assisted design and research

## Future Enhancements

- Multiple-bin monitoring through a central dashboard.
- GPS-based bin location tracking.
- Route optimization for collection vehicles.
- Waste-type classification.
- Mobile application for collection staff.
- Historical analytics and predictive fill-level estimation.

## Learning Outcomes

- Converted a real-world field problem into a technical solution.
- Designed a measurable IoT-based monitoring system.
- Compared sensing approaches and selected a low-cost combination.
- Learned how AI and sensors can support smart waste management.

## Project Presentation

The project presentation is included in this folder.

## Conclusion

The Smart Dustbin addresses the gap between fixed collection schedules and the actual waste level in public bins. By combining ultrasonic sensing, AI-based visual verification, and automatic alerts, the proposed system can help collection teams respond before bins overflow.
