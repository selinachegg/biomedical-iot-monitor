# Biomedical IoT Monitor — BITalino & Pulse Sensor

A prototype system for real-time physiological signal acquisition (heart rate / ECG) using BITalino devices or Arduino pulse sensors, with live upload to [ThingSpeak](https://thingspeak.com).

> **Python 3 required.** The ThingSpeak upload code uses `urllib.parse`, which is not available in Python 2.

---

## Hardware Required

- **BITalino (R)evolution** board — multichannel biosignal acquisition over Bluetooth
- **Arduino** with an analog pulse sensor wired to pin A0
- Host computer running **Windows or Linux** with Bluetooth support

---

## Acquisition Pipelines

### 1. BITalino → Python → ThingSpeak

`bitalino/bitalino.py` connects to the BITalino board via Bluetooth (or serial / Wi-Fi), starts multichannel acquisition at up to 1000 Hz, validates each frame with CRC, and uploads data to ThingSpeak.

```bash
cd bitalino
python bitalino.py
```

### 2. Pulse Sensor → Arduino → Serial → Python → ThingSpeak

`Heartb/Heartb.ino` reads a pulse sensor on analog pin A0, computes BPM using an interrupt-driven algorithm, and streams values over serial at 115200 baud.
`Heartbeat/Heartb_python.py` reads the serial stream and POSTs each BPM value to ThingSpeak.

```bash
python Heartbeat/Heartb_python.py
```

### 3. Bluetooth RFCOMM Data Logger

`ex_master1.py` connects to a Bluetooth device via RFCOMM, collects 100 heart-rate readings, and appends them to `data.txt`.

```bash
python ex_master1.py
```

Output format in `data.txt` (semicolon-delimited):
```
Date;Hour;Minute;Second;HeatBeat;
2024-01-01 12:00:00.000000;72
```

> **Note:** `data.txt` is opened in **append mode** on every run and is never cleared between sessions. The current implementation also writes the header row before every data row, producing a non-standard CSV layout. Post-process accordingly.

---

## Configuration

The following values are hardcoded and must be updated before running. Line numbers are accurate as of the initial commit and may shift if the files are edited.

| File | Line | What to set |
|------|------|-------------|
| `bitalino/bitalino.py` | 538 | ThingSpeak write API key (`key`) |
| `bitalino/bitalino.py` | 556 | BITalino device MAC address (`macAddress`) |
| `Heartbeat/Heartb_python.py` | 5 | Arduino serial port (`/dev/ttyACM0` on Linux, `COMx` on Windows) |
| `Heartbeat/Heartb_python.py` | 7 | ThingSpeak write API key (`key`) |
| `ex_master1.py` | 16 | Target Bluetooth device MAC address |

---

## Dependencies

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install pyserial numpy
```

For Bluetooth connectivity:
```bash
pip install pybluez
# Linux also requires the system Bluetooth headers:
# sudo apt install libbluetooth-dev
```

Install the BITalino library locally:
```bash
cd bitalino
python setup.py install
```

---

## Arduino Sketches

| Sketch | Status | Notes |
|--------|--------|-------|
| `Heartb/Heartb.ino` | Partial | Requires the companion interrupt handler file (`interruptSetup`, `serialOutput`, `serialOutputWhenBeatHappens`). The standard [Pulse Sensor Arduino library](https://github.com/WorldFamousElectronics/PulseSensor_Amped_Arduino) provides these. |
| `BLEapp/BLEapp.ino` | Incomplete | Missing `loop()` body; uses placeholder MAC address (`12:34:56:ab:cd:ef`); depends on the **MediaTek LinkIt LBT library** — not compatible with standard Arduino, ESP32, or other common boards. |

---

## Known Issues

- **Broken HTTP header (silent upload failure):** Both `bitalino/bitalino.py` (line 544) and `Heartbeat/Heartb_python.py` contain a typo in the HTTP Content-Type header: `"Content-typZZe"`. ThingSpeak will not parse the POST body correctly until this is corrected to `"Content-type"`.
- **Duplicate file:** `M5sick_BLE.py` is byte-for-byte identical to `ex_master1.py` and serves no distinct purpose in the current state of the project.

---

## Project Structure

```
miniprojetbell/
├── bitalino/
│   ├── bitalino.py        # BITalino Python SDK + ThingSpeak uploader demo
│   └── setup.py           # Package installer
├── BLEapp/
│   └── BLEapp.ino         # Incomplete BLE client (MediaTek LinkIt LBT library)
├── Heartb/
│   └── Heartb.ino         # Arduino pulse sensor sketch (partial — missing interrupt handlers)
├── Heartbeat/
│   └── Heartb_python.py   # Python serial reader → ThingSpeak uploader
├── ex_master1.py          # Bluetooth RFCOMM logger → data.txt
└── M5sick_BLE.py          # Duplicate of ex_master1.py
```
