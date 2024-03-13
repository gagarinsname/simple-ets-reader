# Simple ETS Reader

This custom implementation is heavily based on source code of Bio-Formats library and specifically on ETS format parsing scheme implemented in it.

The idea is to simplify and speed-up I/O by using python functions and libraries instead of using Bio-Formats python wrapper around the JAVA source code.

Current raw implementation only supports reading *grayscale* videos acquired by certain microscopes alongside with simple meta data.

## Usage

1. Read binary ETS file and its basic metadata
```python
# reads .ets file header and frame addresses
file_path = "input.ets"
sequence = ETSVideo(file_path)
# get video dimensions
num_frames, frame_h, frame_w = sequence.shape
num_frames, frame_h, frame_w # (1, 1920, 1920)
```
2. Access certain frame
```python
# select an index to access
frame_index = 0

img = sequence[frame_index]
img.shape # (1920, 1920)
```