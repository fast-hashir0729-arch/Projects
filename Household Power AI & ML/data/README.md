# Dataset

This project uses the **Individual Household Electric Power Consumption** dataset
from the UCI Machine Learning Repository.

- **Source:** https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption
- **Description:** ~2 million minute-by-minute electrical measurements collected from
  a single household in Sceaux, France between December 2006 and November 2010.
- **File used:** `household_power_consumption.txt`

## Columns

| Column | Description |
|---|---|
| `Date` | dd/mm/yyyy |
| `Time` | hh:mm:ss |
| `Global_active_power` | Household global minute-averaged active power (kW) — **target variable** |
| `Global_reactive_power` | Household global minute-averaged reactive power (kW) |
| `Voltage` | Minute-averaged voltage (V) |
| `Global_intensity` | Household global minute-averaged current intensity (A) |
| `Sub_metering_1` | Energy sub-metering No. 1 — kitchen (Wh) |
| `Sub_metering_2` | Energy sub-metering No. 2 — laundry room (Wh) |
| `Sub_metering_3` | Energy sub-metering No. 3 — water heater & AC (Wh) |

## How to get the data

The raw file is ~130 MB, so it is **not committed to this repository**
(see `.gitignore`). To run the project:

1. Download the zip from the UCI link above (or via `wget`):
   ```bash
   wget https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip -O data/household_power_consumption.zip
   unzip data/household_power_consumption.zip -d data/
   ```
2. Confirm `data/household_power_consumption.txt` exists.
3. Run the pipeline: `python main.py --data data/household_power_consumption.txt`
