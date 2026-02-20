# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A biomedical/IoT prototype for acquiring physiological signals (primarily heart rate/pulse) from hardware sensors, processing them in Python, and uploading data to ThingSpeak for remote monitoring.

## Running Scripts

```bash
# Install the BITalino library
cd bitalino && python setup.py install

# Run BITalino data acquisition with ThingSpeak upload
python M5sick_BLE.py

# Run Bluetooth socket communication example
python ex_master1.py

# Read heartbeat sensor from serial and upload to ThingSpeak
python Heartbeat/Heartb_python.py
```

There are no formal build, lint, or test pipelines. Scripts are run directly with Python.

## Architecture

**Data flow:**
```
[Hardware Sensor] → [Arduino firmware / BITalino] → [Bluetooth / Serial] → [Python script] → [ThingSpeak API]
```

**Key components:**

- `bitalino/bitalino.py` — The core BITalino Python API. Supports Bluetooth (Windows/Linux), Serial, and WiFi connections. Handles data framing, CRC validation, sampling rate, and channel configuration.
- `M5sick_BLE.py` — Connects to a BITalino device via Bluetooth, acquires multichannel physiological data, and POSTs to ThingSpeak.
- `ex_master1.py` — Minimal Bluetooth RFCOMM socket client; logs timestamped heart rate data to `data.txt` (CSV with semicolon delimiter).
- `Heartbeat/Heartb_python.py` — Reads BPM values from an Arduino over serial and uploads to ThingSpeak.
- `BLEapp/BLEapp.ino` — Arduino BLE client firmware (incomplete; placeholder MAC address).
- `Heartb/Heartb.ino` — Arduino pulse sensor sketch using interrupt-driven BPM calculation; communicates at 115200 baud over serial.

## Important Configuration Details

- **Bluetooth MAC addresses** and **ThingSpeak API keys** are hardcoded in the Python scripts. Update them before use:
  - Target BITalino device MAC: `24:A1:60:53:C1:2A` (in `M5sick_BLE.py` and `ex_master1.py`)
  - ThingSpeak write keys in `M5sick_BLE.py` and `Heartbeat/Heartb_python.py`
- ThingSpeak uploads go to `api.thingspeak.com:80` via HTTP POST using field 1.
- CSV output from `ex_master1.py` is written to `data.txt` in format: `Date;Hour;Minute;Second;HeartBeat;`

## Known Incomplete Areas

- `BLEapp/BLEapp.ino` is missing the `loop()` function body and uses a placeholder MAC address.
- `Heartb/Heartb.ino` references interrupt handler functions that are not present in the file.
