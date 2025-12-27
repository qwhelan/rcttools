# rct2gpx

rct2gpx is a command line tool for extracting data from Garmin Varia RCT715 rear radar/camera devices. The video files created by this device have data embedded in the footage and are not in a machine readable format.

This tool attempts to extract time and GPS coordinates into a GPX file to allow better processing of the footage. Bike speed and approaching vehicle speed will be added in a future release.

# Extraction Process

## ffmpeg-based Cropping and Thresholding

The data is embedded as white text with a black border. Unfortunately, a common background is asphalt from roads and white road markings, both of which interfere with a straight OCR of the raw footage.

Instead, we use ffmpeg's threshold filter to extract only the pure white pixels, setting all others to black. We then invert all pixels to get black text on a white background, to assist OCR.

## Data update detection model

The Garmin Varia RCT715 records footage at ~30fps and receives data updates from the head unit at ~1Hz, which leads to variability in the number of frames between updates. In practice, this varies between [29, 32] frames, inclusive.

A data update consists of the following changes:
 - time (increment by 1 or more seconds, some seconds can get skipped)
 - GPS lat/long (potentially no change)
 - Bike speed (potentially no change)
 - Approaching vehicle speed (potentially no change)

 Additionally, all values can disappear entirely in the event the Varia loses connection with the head unit or was turned on independent of the head unit. Finally, the last value can appear/disappear based on road conditions.

 As a result, we are only guaranteed that the first field will change with a given data update. The least significant digit of the time field appears to have a consistent horizontal location, which allows for a restricted model to identify which frame indicates a data update.

 ## Fixed-width format

 The data uses an approximately fixed-width format, with digits separated by 22 pixels in the original format and alternating 20/22 pixels in the current format. Additionally, the current format is shifted one pixel up compared to the original one.

 | Character type | v0 width | v1 width | v1 parity | 
 | -------------- | -------- | -------- | --------- |
 | Digit | 22 | 21 | yes |
 | Symbol (/:.-) | 16 | 16 | no |
 | Space | 10 | 10 | no |

Due to the consistent but variable widths of characters, a small state machine class is used to track the horizontal offset of the next character to detect. In the v1 format, parity is tracked across the entire data update and adjusts the width of digits by +1/-1.

As the least significant time digit is not impacted in its horizontal position, we use the prior step to identify whether the one pixel vertical offset of v1 format is in effect. Once v0/v1 is determined, the state machine can either ignore (v0) or adopt (v1) the parity logic.

 ## Frame Stacking

 With a good sense of when data changes happened, we can now stack all of the frames with the same data to help remove any background noise.

 ## Character detection

 Working on the stacked frames, we can now process ~30 frames at once and utilize the v0/v1 state machine to identify the appropriate horizontal/vertical offset for the next character.

 Each character has been extracted as a PNG in `rcttools/alphabet/` and the candidate character is converted into a bitmap and `np.logical_and()`'d with each relevant character in the alphabet, which is a function of the state machine. This score is normalized by the `np.logical_or()` of the character with the candidate and the top character from the alphabet is used.

 In general, a score of ~0.95 is expected from a good quality match; a score of less than 0.8 indicates no good match (likely no data whatsoever).

 ## Validation

This is not yet implemented, but given the head unit records a GPX file of its own, the results from this process can be cross-checked against the head unit file. One complication is that the embedded data is truncated to have one less digit in the latitude/longitude so any comparison would need to incorporate rounding.

 # Features in future releases

 - Bike/vehicle speed data
 - GPX validation against head unit
 - Concatenation of data for sequential video files
 - Ability to emit full video frames corresponding to data updates
 - Generate masks for embedded data to support computer vision use cases

# Developing

## Tests
```
$ uv run -m pytest
```
