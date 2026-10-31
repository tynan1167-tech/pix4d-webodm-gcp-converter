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
