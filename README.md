# pix4d-webodm-gcp-converter
Project: Recovering Legacy Pix4D GCP Data for Open-Source Photogrammetry
# Pix4D to WebODM GCP Converter

Recover Ground Control Point (GCP) observations from Pix4D project exports and convert them into WebODM-compatible GCP files.

## Background

WebODM requires GCP files in the format:

```text
EPSG:6597
geo_x geo_y geo_z im_x im_y filename label
```

Many legacy Pix4D projects contain surveyed coordinates but not readily accessible image-space observations.

This tool extracts:

- GCP IDs (MTP_3000, MTP_3001, etc.)
- Pixel coordinates
- Associated image names
- Survey coordinates

and automatically generates a WebODM-compatible GCP file.

## Example

Pix4D Export:

```text
MTP_3000 2239.51 98.2832 1
-99
Shoreline Place 0055
```

Output:

```text
275462.7713 1267516.9328 415.9350 2239.51 98.2832 Shoreline%20Place%200055.JPG 3000
```

## Workflow

```text
Pix4D Project
      │
      ▼
Project_tp_pix4d.txt
      │
      ▼
Extract MTP Observations
      │
      ▼
Match Survey Coordinates
      │
      ▼
WebODM GCP File
```

## Requirements

```bash
python >= 3.10
```

## Usage

```bash
python build_webodm_gcps.py \
    --pix4d Project_tp_pix4d.txt \
    --output webodm_gcps.txt
```

## Coordinate Table

Example:

```python
CONTROL_POINTS = {
    "3000": (275462.7713,1267516.9328,415.9350),
    "3001": (275483.0068,1266777.3401,462.7050),
}
```

## Use Cases

- Pix4D → WebODM Migration
- Legacy Project Recovery
- Open Source Photogrammetry Workflows
- UAS Survey Projects
- GIS Portfolio Demonstrations

## Author

Developed as part of UAS and GIS workflow modernization efforts focused on photogrammetry, survey control, and open-source processing.
