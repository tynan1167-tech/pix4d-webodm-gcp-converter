## Project Status

🚧 Research & Development

This project is an investigation into recovering Ground Control Point (GCP) observations from legacy Pix4D projects and converting them into formats compatible with WebODM/OpenDroneMap.

Current Status:
- ✅ GCP coordinate recovery
- ✅ MTP observation recovery
- ✅ Pix4D project parsing
- ✅ WebODM GCP generation
- ⚠️ Image filename mapping under investigation
- ⚠️ End-to-end migration not yet validated

Project: Recovering Legacy Pix4D GCP Data for Open-Source Photogrammetry

Recovering and converting legacy Pix4D GCP observations for open-source photogrammetry workflows.

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

## Lessons Learned

### Pix4D Stores More Information Than Expected

Although standard GCP exports provide only surveyed coordinates, the `tp_pix4d.txt` file contains image-space observations used during bundle adjustment.

Example:

```text
MTP_3000 2239.51 98.2832 1
```

These records preserve the image measurements necessary for reconstructing GCP observations.

---

### Reverse Engineering Proprietary Formats

Recovering GCP observations required:

- Investigating Pix4D project exports
- Parsing a 4.8+ million record file
- Identifying MTP records
- Reconstructing links between image observations and surveyed points

---

### Filename Mapping is Non-Trivial

A major challenge encountered was determining how Pix4D references imagery internally.

Example:

```text
Shoreline Place 0055
```

appears to identify an image, but initial WebODM testing suggests this label may not directly correspond to the image filename expected during processing.

---

### WebODM Validation

WebODM successfully:

- Parsed the generated GCP files
- Accepted EPSG:6597 coordinates
- Detected control points

However, image matching failed because image references could not be resolved.

Future work will focus on validating filename reconstruction and creating a fully automated migration workflow.

## Open Research Questions

- How does Pix4D store image filename references internally?
- Can image labels be reliably mapped to original filenames?
- Can a fully automated Pix4D → WebODM migration workflow be created?
- Can bundle adjustment metadata be exported directly from Pix4D projects?

## Investigation Log
### October 2026

Recovered MTP-based GCP observations from a legacy Pix4D project.

Observed records:

MTP_3000 2239.51 98.2832 1

Successfully reconstructed:

- GCP IDs
- Image-space coordinates
- Survey coordinates

Generated valid WebODM GCP syntax but encountered unresolved image filename matching issues.

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

## Tynan Conner

Developed as part of UAS and GIS workflow modernization efforts focused on photogrammetry, survey control, and open-source processing.
┌──────────────────┐
│ Pix4D Project    │
│ (.p4d)           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ tp_pix4d.txt     │
│ 4.8M+ rows       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Detect MTPs      │
│ MTP_3000-3009    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Extract          │
│ Pixel Locations  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Match Surveyed   │
│ GCP Coordinates  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate         │
│ WebODM GCP File  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ WebODM           │
│ Photogrammetry   │
└──────────────────┘
# build_webodm_gcps.py

import re

PIX4D_FILE = "Project_3_tp_pix4d.txt"
OUTPUT_FILE = "webodm_gcps.txt"

CONTROL_POINTS = {
    "3000": (275462.7713,1267516.9328,415.9350),
    "3001": (275483.0068,1266777.3401,462.7050),
    "3002": (274755.6735,1267218.9227,439.0990),
    "3003": (275252.8693,1266958.7504,450.8850),
    "3004": (275047.4422,1267428.5328,438.2870),
    "3005": (275235.2637,1267609.5425,420.7820),
    "3006": (275240.9334,1267177.9724,442.1180),
    "3007": (275362.2080,1267197.8258,439.5010),
    "3008": (275231.7910,1267406.1879,437.2780),
    "3009": (275059.6725,1267088.2269,456.1390),
}

mtp_pattern = re.compile(
    r'^MTP_(300[0-9])\s+([\d\.]+)\s+([\d\.]+)'
)

with open(PIX4D_FILE, encoding="utf-8") as f:
    lines = [line.strip() for line in f]

output = ["EPSG:6597"]

for i, line in enumerate(lines):

    match = mtp_pattern.match(line)

    if not match:
        continue

    gcp = match.group(1)
    im_x = match.group(2)
    im_y = match.group(3)

    image_name = None

    for j in range(i + 1, min(i + 20, len(lines))):

        if lines[j].startswith("Shoreline Place"):

            image_name = (
                lines[j]
                .replace(" ", "%20")
                + ".JPG"
            )
            break

    if image_name is None:
        continue

    geo_x, geo_y, geo_z = CONTROL_POINTS[gcp]

    output.append(
        f"{geo_x} {geo_y} {geo_z} "
        f"{im_x} {im_y} "
        f"{image_name} {gcp}"
    )

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print(f"Written: {OUTPUT_FILE}")
