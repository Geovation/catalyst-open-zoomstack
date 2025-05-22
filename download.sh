#!/bin/bash

# URL to download the file from
URL="https://api.os.uk/downloads/v1/products/OpenZoomstack/downloads?area=GB&format=Vector+Tiles&subformat=%28MBTiles%29&redirect"

# Output file name
OUTPUT="osopenzoomstack.mbtiles"

rm -f "$OUTPUT"

# Use curl to download the file
curl -L -o "$OUTPUT" "$URL"

echo "Download completed and saved to $OUTPUT"