# Message Queuing Telemetry Transport Protocol Repository

This repository contains a series of Python scripts (`*.py` files), each designed to address specific problems related to MQTT (Message Queuing Telemetry Transport) protocol. Below is a description of each script and the problem it solves:

## 1. `1_Broker.py`
**Problem 1: Broker Management**
- This script is responsible for managing a broker in the MQTT system. The broker handles publications and subscriptions of various elements that connect to it. The script ensures connectivity to the broker at simba.fdi.ucm.es and facilitates sending and receiving messages in the `clients` topic. It also supports creating hierarchical channels from this root topic.

## 2. `2_Numbers.py`
**Problem 2: Number Processing**
- This script is an MQTT client designed to read from the `numbers` topic, where integers and real numbers are constantly published. It separates integers from real numbers, calculates their frequencies, and analyzes properties of the integers (like primality).

## 3. `3_Temperature.py`
**Problem 3: Temperature Monitoring**
- This MQTT client script reads from the `temperature` topic, which may have multiple sensors emitting values. It calculates the maximum, minimum, and average temperature for each sensor and across all sensors within a specified short time interval (between 4 and 8 seconds).

## 4. `4_Humidity.py`
**Problem 4: Temperature and Humidity Monitoring**
- This script focuses on a specific thermometer within the `temperature` topic. The MQTT client listens to this thermometer and, upon detecting a temperature exceeding a predefined threshold (K0), starts listening to the `humidity` topic as well. It stops listening to `humidity` if the temperature falls below K0 or humidity exceeds K1.

## 5. `5_Timer.py`
**Problem 5: MQTT Timer Client**
- This script acts as a timer. The MQTT client reads messages indicating a waiting time, a topic, and a message to be published after the waiting period. The client waits for the specified duration and then publishes the message in the designated topic.

## 6. `6_Different_Clients_.py`
**Problem 6: Chaining Client Behaviors**
- This script is designed to chain the behaviors of different MQTT clients based on the solutions provided in the previous scripts. For example, a client might listen for numbers and, under certain conditions (like receiving a prime number), set an alarm on the timer, and then listen to the `humidity` topic to calculate an average value. This script demonstrates the potential for complex interactions and behaviors among different MQTT clients.

Each script in this repository is a standalone solution to its respective problem, showcasing various aspects and capabilities of MQTT clients in different scenarios.
