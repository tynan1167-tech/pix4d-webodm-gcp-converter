# Pix4D GCP Recovery & WebODM Conversion Investigation

Recovering and converting legacy Pix4D Ground Control Point (GCP) observations for open-source photogrammetry workflows.

🚧 Research & Development Project

## Project Status

Current Status:

- ✅ GCP coordinate recovery
- ✅ MTP observation recovery
- ✅ Pix4D project parsing
- ✅ Preliminary WebODM GCP generation
- ✅ Multi-million record file analysis
- ⚠️ Image filename mapping under investigation
- ⚠️ End-to-end migration not yet validated

## Problem Statement

A legacy drone mapping project was originally processed using Pix4Dmapper.

Although surveyed Ground Control Point (GCP) coordinates remained available, access to Pix4D software was no longer available. The objective of this project was to determine whether image-space GCP observations could be recovered directly from Pix4D project exports and converted into formats compatible with WebODM/OpenDroneMap.

This effort evolved into a broader investigation of Pix4D's internal project structure, GCP storage methods, and interoperability challenges with open-source photogrammetry workflows.

## Background

WebODM requires GCP files in the format:

```text
EPSG:6597
geo_x geo_y geo_z im_x im_y filename label
```

Many legacy Pix4D projects contain surveyed coordinates but do not expose the image-space observations in a straightforward format. This project explored whether those observations remained embedded in exported project data and whether they could be reconstructed into a usable WebODM control-point input.

The investigation focused on:

- Recovering GCP observations from legacy Pix4D project exports
- Parsing large Pix4D text outputs
- Matching image-space measurements to surveyed coordinates
- Evaluating compatibility with WebODM/OpenDroneMap processing

## Investigation Findings

### Pix4D Stores More Information Than Expected

Although standard GCP exports provide only surveyed coordinates, the `tp_pix4d.txt` file contains image-space observations used during bundle adjustment.

Example:

```text
MTP_3000 2239.51 98.2832 1
```

These observations preserve the image measurements necessary for reconstructing GCP records.

### Reverse Engineering Proprietary Formats

Recovering GCP observations required:

- Investigating Pix4D project exports
- Parsing a 4.8+ million record file
- Identifying MTP records
- Reconstructing links between image observations and surveyed points

### Filename Mapping Is Non-Trivial

A major challenge encountered was determining how Pix4D references imagery internally.

Example:

```text
Shoreline Place 0055
```

This label appears to identify an image, but the exact relationship to the original image filename remains under investigation. WebODM requires precise filename matching, which means image label reconstruction is a critical interoperability issue.

### WebODM Validation

WebODM successfully:

- Parsed the generated GCP files
- Accepted EPSG:6597 coordinates
- Detected control points

However, image matching failed because image references could not be resolved consistently. This indicates that the recovered coordinate data is viable, but a complete migration workflow still requires additional filename reconstruction.

## Technical Challenges

The following challenges were encountered during development:

### Parsing Large Datasets

One project export contained over 4.8 million observation records, requiring automated filtering and targeted extraction of relevant GCP measurements.

### Filename Resolution

Recovered observations referenced image labels such as:

```text
Shoreline Place 0055
```

However, WebODM requires exact filename matching, and the original filename mapping remains under investigation.

### Platform Interoperability

Pix4D and WebODM represent GCP observations differently, requiring translation between proprietary and open-source photogrammetry formats.

## Workflow

```text
Pix4D Project
      │
      ▼
Project_tp_pix4d.txt
      │
      ▼
Extract MTP observations
      │
      ▼
Match surveyed GCP coordinates
      │
      ▼
Generate preliminary WebODM GCP records
      │
      ▼
Validate in WebODM workflow
```

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

## Research Questions

- How does Pix4D store image filename references internally?
- Can image labels be reliably mapped to original filenames?
- Can a fully automated Pix4D → WebODM migration workflow be created?
- Can bundle adjustment metadata be exported directly from Pix4D projects?

## Investigation Log

### October 2026

Recovered MTP-based GCP observations from a legacy Pix4D project.

Observed records included:

```text
MTP_3000 2239.51 98.2832 1
```

Successfully reconstructed:

- GCP IDs
- Image-space coordinates
- Surveyed control coordinates

Generated valid WebODM GCP syntax but encountered unresolved image filename matching issues.

## Use Cases

- Pix4D → WebODM migration
- Legacy project recovery
- Open-source photogrammetry workflows
- UAS survey projects
- GIS and geospatial portfolio development
- Photogrammetry interoperability research

## Future Development

Planned next steps include:

- Recover original image filename references
- Improve parser accuracy
- Create automated Pix4D → WebODM conversion
- Validate workflow using smaller test datasets
- Support additional Pix4D export formats
- Package the converter as a standalone Python utility

## Python Prototype

A prototype parser has been developed to:

- Parse Pix4D `tp_pix4d.txt` exports
- Extract MTP observations
- Associate observations with surveyed coordinates
- Generate preliminary WebODM GCP records

Source:

```text
scripts/build_webodm_gcps.py
```

## Technologies Used

- Python
- PowerShell
- Pix4Dmapper
- OpenDroneMap
- WebODM
- OpenSfM
- Ground Control Points (GCPs)
- UAS Photogrammetry
- Coordinate Reference Systems (EPSG:6597)

## Author

Tynan Conner

Developed as part of independent work exploring UAS photogrammetry, survey control workflows, GIS automation, and open-source geospatial processing.

---
