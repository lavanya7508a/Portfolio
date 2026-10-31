SECOND REVIEW REPORT

Project Title: AI-Based Smart Dustbin Monitoring System

1.  PROJECT OVERVIEW

The project is a Smart Waste Bin Monitoring and AI-Based Overflow
Detection System designed to address overflowing public waste bins and
inefficient waste collection. A field study was conducted in Goundanur,
where overflowing public bins, lack of proper wet/dry waste segregation,
and limited daily collection were observed.

The proposed system uses an ESP32 microcontroller and HC-SR04 ultrasonic
sensor to estimate the fill level of a dustbin. When the fill level
reaches an initial threshold of 80%, the system generates an alert
indicating that the bin requires collection. A future AI module will
detect visible waste overflow using images and object-detection
techniques.

At the Review 2 stage, approximately 35% of the project has been
completed, covering field study, problem identification, objectives,
system architecture, hardware selection, sensing methodology, alert
logic, algorithm design, prototype planning, and technical
documentation.

2.  PROBLEM STATEMENT

Public waste bins can become full or overflow before the next scheduled
collection. Manual monitoring of every bin is difficult, while fixed
collection schedules do not always reflect the actual condition of each
bin. Overflowing waste can create unhygienic surroundings.

The proposed solution is an automated monitoring system that identifies
the fill condition of a bin and provides an early alert before
significant overflow occurs.

3.  OBJECTIVES

The main objectives are: • Automatically monitor waste-bin fill level. •
Use an HC-SR04 ultrasonic sensor to measure the distance to the waste
surface. • Interface the sensor with an ESP32. • Convert measured
distance into an estimated fill percentage. • Generate an alert when the
fill level reaches approximately 80%. • Reduce continuous manual
inspection. • Support condition-based waste collection. • Develop a
future AI module for visible overflow detection. • Provide a foundation
for multiple smart bins.

4.  SYSTEM ARCHITECTURE

The basic architecture is:

Waste Bin → HC-SR04 → ESP32 → Distance Measurement → Fill-Level
Calculation → 80% Threshold → Alert

The ultrasonic sensor is positioned near the top of the bin. It sends an
ultrasonic pulse toward the waste surface and measures the returning
echo. The ESP32 calculates the distance and converts it into a fill
percentage using the known effective height of the bin.

If the calculated fill level is 80% or greater, the system identifies a
critical condition and generates an alert.

5.  HARDWARE COMPONENTS

The planned prototype consists of: • ESP32 – main controller for reading
and processing sensor data. • HC-SR04 ultrasonic sensor – measures
distance to the waste surface. • Dustbin – physical environment for
testing. • Breadboard and jumper wires – used for prototype assembly. •
Alert/output mechanism – indicates the critical fill condition.

6.  FILL-LEVEL CALCULATION

The fill percentage can be calculated using:

Fill Percentage = ((Bin Height - Measured Distance) / Bin Height) × 100

For example, if the effective bin height is 50 cm and the measured
distance is 10 cm:

Fill Percentage = ((50 - 10) / 50) × 100 Fill Percentage = 80%

The actual values will be calibrated according to the dimensions and
sensor position of the physical dustbin.

7.  ALERT LOGIC

The initial threshold is 80%. • Below 80% – Normal condition. • At or
above 80% – Critical condition and alert.

The threshold can be adjusted after physical testing. The purpose is to
provide an early warning so collection can take place before the bin
reaches complete capacity.

8.  ALGORITHM / PSEUDOCODE

START Initialize ESP32 and HC-SR04. Set the known bin height.

Repeat: Send ultrasonic pulse. Read echo time. Calculate distance.
Calculate fill percentage.

    If fill percentage >= 80%:
        Generate alert.
    Else:
        Continue normal monitoring.

    Display distance and fill percentage.

Repeat. STOP

9.  CURRENT PROJECT STATUS

The following work has been completed for the 35% stage: • Field study
and real-world problem identification. • Problem statement and
objectives. • Proposed system architecture. • ESP32 and HC-SR04
component selection. • Fill-level measurement concept. • Fill percentage
calculation method. • 80% threshold alert logic. • Algorithm and
pseudocode. • Prototype planning. • AI overflow-detection concept. •
Technical and project documentation.

The documentation clearly separates the proposed design from features
that are still under implementation.

10. AI-BASED OVERFLOW DETECTION

The project also proposes an AI-based image detection module to identify
visible overflow.

The planned workflow is:

Camera/Image → Image Processing → Object/Overflow Detection →
Classification → Alert

An object-detection approach such as YOLO may be used. Possible
categories include normal bin, nearly full bin, overflowing bin, and
waste outside the bin.

This AI component is currently part of the planned development and will
be implemented and tested in the next stage.

11. TESTING PLAN

The prototype will be tested under different fill conditions: • Empty
bin – low fill percentage and normal status. • Partially filled bin –
intermediate fill percentage. • Approximately 80% filled bin – threshold
alert. • Overflow condition – critical/overflow indication.

Serial-monitor output will be captured to demonstrate actual distance
and fill-level readings.

Expected output:

Distance: 35 cm Fill Level: 30% Status: NORMAL

Distance: 20 cm Fill Level: 60% Status: NORMAL

Distance: 10 cm Fill Level: 80% Status: ALERT - BIN 80% FULL

Actual readings will depend on the physical bin dimensions and sensor
position.

12. AREAS FOR IMPROVEMENT AND NEXT STEPS

The immediate next steps are: 1. Develop and upload a working
Arduino/ESP32 .ino sketch to read the HC-SR04, calculate distance and
fill percentage, and trigger the 80% alert. 2. Create the actual
circuit/schematic showing the HC-SR04 and ESP32 pin connections. 3.
Assemble the circuit on a breadboard and mount the sensor on an actual
dustbin. 4. Capture photographs of the physical prototype and wiring. 5.
Capture serial-monitor evidence showing distance, fill percentage, and
alert status. 6. Begin AI overflow detection by preparing a labelled
sample image dataset and/or an initial YOLO/object-detection
implementation.

13. FUTURE SYSTEM

The final system is intended to combine sensor-based monitoring with
AI-based visual detection.

Ultrasonic Sensor → ESP32 → Fill-Level Monitoring → Alert

Camera → AI Detection → Visible Overflow Detection → Alert

In the future, multiple smart bins could send their status to a
centralized monitoring platform. This could help sanitation authorities
identify bins requiring collection and improve collection efficiency.

14. CONCLUSION

The Review 2 stage has established a clear foundation for the Smart
Waste Bin Monitoring and AI-Based Overflow Detection System. The project
has progressed from real-world field observation to a defined technical
solution using an ESP32 and HC-SR04 ultrasonic sensor.

The system architecture, objectives, hardware selection, fill-level
calculation, 80% threshold logic, algorithm, pseudocode, prototype plan,
and AI integration concept have been completed as part of the 35%
project stage.

The major remaining work is practical implementation: developing the
ESP32 code, building and documenting the physical circuit, collecting
live sensor readings, and starting the AI-based overflow detection
module. These steps will provide implementation evidence and move the
project from design and documentation toward a tested working prototype.

CURRENT STATUS: 35% DESIGN AND DOCUMENTATION STAGE COMPLETED. HARDWARE
IMPLEMENTATION, LIVE SENSOR TESTING, AND AI OVERFLOW DETECTION ARE THE
NEXT DEVELOPMENT PRIORITIES.
