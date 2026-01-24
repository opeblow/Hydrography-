# Hydrography - Tidal Datum Transfer Analysis

A Python toolkit for calculating and visualizing tidal datum transfers between tide gauge stations along the Nigerian coast (Lagos Bar, Escravos Bar, Bonny River Bar).

## Overview

Datum transfer is a fundamental hydrographic technique used to establish the vertical relationship between tide gauges at different locations. This project calculates the Mean Sea Level (MSL) difference between stations, enabling depth measurements from one station to be converted to another's reference datum.

## Features

- **Datum Transfer Calculation**: Computes MSL difference between two stations with 95% confidence uncertainty
- **Tidal Statistics**: Calculates MHW, MLW, tidal range, and standard deviation
- **Visualization**: Generates comparative tidal curve plots with MSL reference lines
- **Multi-station Support**: Handles Lagos, Escravos, and Bonny River Bar stations

## Project Structure

```
Hydrography-/
├── data/                           # Excel files with tide observations
│   ├── Tide_Data_Lagos_Escravos_May2026.xlsx
│   ├── Tide_Data_Lagos_Escravos_September2026.xlsx
│   └── Tide_Data_Bonny_River_Bar_Escravos_Bar_may2026.xlsx
├── datum_transfers/                # Analysis modules
│   ├── __init__.py
│   ├── transfer_1.py               # Lagos ↔ Escravos (May)
│   ├── transfer_2.py               # Lagos ↔ Escravos (September)
│   ├── transfer_3.py               # Bonny River ↔ Escravos
│   └── visualize_tides.py          # Tidal curve visualization
├── plots/                          # Generated visualization outputs
│   ├── lagos_escravos_may2026.png
│   ├── lagos_escravos_september2026.png
│   └── bonny_escravos_may2026.png
├── requirements.txt
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/opeblow/Hydrography-.git
cd Hydrography-

# Install dependencies
pip install -r requirements.txt
pip install openpyxl  # Required for Excel file reading
```

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- openpyxl

## Data Format

Excel files should contain two sheets (one per station) with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Date | Observation date | 1/5/26 |
| Time | Observation time (HH:MM) | 05:35 |
| Height(m) | Tide height in meters | 2.1 |
| Tide_Type | HW (High Water) or LW (Low Water) | HW |

## Usage

### Calculate Datum Transfer

```bash
# Run individual transfer calculations
python datum_transfers/transfer_1.py  # Lagos-Escravos May
python datum_transfers/transfer_2.py  # Lagos-Escravos September
python datum_transfers/transfer_3.py  # Bonny-Escravos
```

### Generate Visualizations

```bash
python datum_transfers/visualize_tides.py
```

This generates PNG plots in the `plots/` directory showing:
- Both stations' tidal curves on the same graph
- DateTime on X-axis, Height (m) on Y-axis
- Dashed horizontal lines for each station's MSL
- Datum transfer value in the title

### Example Output

```
DATUM TRANSFER CALCULATION
============================================================
Bonny River Bar MSL:     1.355 m
Escravos Bar MSL:        0.917 m

DATUM TRANSFER: +0.438 m ± 0.023 m

Bonny River Bar CD is 0.438 m HIGHER than Escravos Bar CD
To convert Bonny to Escravos: SUBTRACT 0.438 m
============================================================
```

## Methodology

1. **Load Data**: Parse Excel files, combine Date + Time into DateTime
2. **Calculate Statistics**: 
   - MSL = mean of all height observations
   - MHW = mean of High Water observations
   - MLW = mean of Low Water observations
   - Tidal Range = MHW - MLW
3. **Compute Datum Transfer**: 
   - DT = MSL₁ - MSL₂
   - Uncertainty = 1.96 × √(σ₁²/n₁ + σ₂²/n₂)

## Stations

| Station | Location | Description |
|---------|----------|-------------|
| Lagos Bar | Lagos, Nigeria | Primary reference station |
| Escravos Bar | Delta State, Nigeria | Secondary station |
| Bonny River Bar | Rivers State, Nigeria | Tertiary station |

## License

MIT License

## Author

[opeblow](https://github.com/opeblow)
