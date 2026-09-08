# Report

Project Title

Smart Dustbin – AI-Enabled Fill-Level Monitoring System

1. Introduction

The Smart Dustbin project is a proposed smart waste-management solution designed to monitor the fill level of public dustbins in real time and alert collection teams before the bins overflow. The project was initiated based on a field study conducted at Goundanur, Coimbatore.

During the field observation, overflowing bins were noticed by midday near the entrance. It was also observed that there was no wet/dry waste segregation at the site and that waste collection was carried out once a day before peak demand. These observations indicated a gap between the actual waste level and the fixed collection schedule.

2. Problem Statement

Public dustbins may overflow before the next scheduled collection because collection is based on a fixed schedule rather than the actual fill level of individual bins. This can lead to waste spilling into surrounding areas, unhygienic conditions, pest attraction and poor waste-management conditions. The project therefore aims to provide real-time information about the condition of the dustbin and enable timely collection.

3. Objectives

The main objectives identified for the project are:

To detect the fill level of the dustbin in real time.
To generate an alert when the bin reaches approximately 80% capacity.
To reduce the occurrence of waste overflow.
To reduce the response time between an alert and waste collection.
To continuously log fill-level information and identify peak-fill periods for future demand-based collection planning.
4. Existing System Analysis

Three existing approaches were considered: fixed-schedule collection, manual inspection and public complaint reporting.

Fixed-schedule collection does not consider the actual fill level of individual bins. Manual inspection requires workers to physically check the bins and may be infrequent. Public complaint reporting is reactive because action generally begins only after residents notice the overflow. The major gap identified is the absence of an affordable system that provides automatic, real-time visibility of the bin's fill condition.

5. Proposed Solution

The proposed solution is a Smart Dustbin with Fill Sensing and Vision-Based Overflow Detection.

An ultrasonic sensor will be used to measure the distance between the sensor and the waste surface and estimate the fill percentage. An ESP32 microcontroller will process the sensor readings. A camera and object-detection model are proposed to visually identify and verify waste overflow or spillage.

The system will use Wi-Fi or GSM communication to send the status or alert to a dashboard or collection team's phone. The combination of ultrasonic sensing and camera-based verification is intended to provide more reliable monitoring and reduce false alerts.

6. System Architecture

The proposed system consists of four major stages:

Data Source → Processing → Communication → Interface

The ultrasonic sensor installed near the dustbin lid acts as the data source. The ESP32 processes the sensor reading and calculates the approximate fill percentage. When the predefined threshold is reached, Wi-Fi/GSM can transmit the alert. The dashboard or SMS interface allows the collection team to receive the information and take appropriate action.

After the bin is serviced, monitoring continues automatically.

7. Prototype Development

At the current 35% project stage, the prototype concept and system architecture have been designed. The major components identified are:

Smart dustbin
Ultrasonic sensor
ESP32 microcontroller
Camera
Wi-Fi/GSM communication
Power supply
AI-based object-detection component

The ultrasonic sensor is planned to be positioned near the top of the dustbin to monitor the waste level. The ESP32 will process the sensor readings and determine whether the bin has reached the 80% alert threshold. The camera-based AI component is planned to provide additional visual confirmation of overflow.

8. AI Component

The proposed AI component is based on object detection. The model will use labelled images of overflowing dustbins, with bounding boxes identifying the bin and spilled waste. The trained model is intended to identify visible overflow and provide an additional verification signal.

At the 35% stage, the AI methodology and training-data concept have been identified. Dataset preparation, model training and performance evaluation are part of the next development stage.

9. Current Progress – 35%

The following activities have been completed or defined during the current review stage:

Field problem identification
Field observation
Problem statement preparation
Objective definition
Existing-system analysis
Proposed solution selection
Hardware component identification
AI approach identification
System architecture design
Prototype concept development
Feasibility and risk analysis

The current stage represents the problem identification, analysis, solution design and prototype-planning phase of the project.

10. Expected Outcomes

The proposed system aims to change the collection trigger from a fixed schedule to the actual fill level of the bin. The project targets a reduction in overflow incidents and aims to reduce the alert-to-pickup response time to under two hours. It will also provide continuous fill-level visibility that can later support better collection planning. These are project targets and have not yet been presented as measured final results.

11. Feasibility and Risk Management

The proposed system is considered suitable for prototype development because it uses a limited number of hardware components such as an ultrasonic sensor, ESP32, camera and communication system.

One identified risk is sensor fouling caused by dust, moisture or waste. This can be addressed using protective housing and a regular sensor-cleaning schedule. Further testing will be required to validate sensor accuracy and system reliability.

12. Future Work

The next stage of the project will focus on:

Hardware assembly.
Ultrasonic sensor integration and calibration.
ESP32 programming.
Camera integration.
Dataset collection and labelling.
AI object-detection model training.
Wi-Fi/GSM alert implementation.
Dashboard development.
Prototype testing.
Field testing and performance evaluation.
13. Conclusion

The Smart Dustbin project addresses the problem of waste overflow caused by fixed collection schedules. The field study helped identify the real-world problem, and the proposed solution combines ultrasonic fill-level sensing, ESP32 processing, communication and AI-based visual overflow detection.

At the 35% completion stage, the project has successfully established the problem, objectives, proposed solution, system architecture, component selection and prototype design. The next phase will focus on implementing and testing the physical prototype, AI model and alert system.

The project ultimately aims to provide a practical, low-cost and intelligent approach to waste management by enabling collection teams to respond to the actual condition of dustbins rather than relying only on fixed schedules.

14. Project Status

Current Status: 35% – Review 1

Completed: Problem identification, field study, requirements, proposed solution, technology selection, architecture and prototype planning.
