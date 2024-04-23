# Simple ETS Reader

This custom implementation is heavily based on the source code of the Bio-Formats library, specifically on the ETS format parsing scheme implemented in it.

The goal is to simplify and speed up I/O by utilizing Python functions and libraries, rather than using the Bio-Formats Python wrapper around the JAVA source code.
Additionally, this tool can be helpful for those who wish to recover raw data from an ETS file when the VSI file is lost.

The current raw implementation supports only the reading of grayscale videos acquired by certain microscopes, along with simple metadata from the ETS file.
As of now, parsing stored image pyramids is not supported.


## Installation

1. Prerequisites:
- Anaconda OR python>=3.8 installed on your machine.
- All the necessary dependencies listed in requirements.txt.

2. To install these requirements, clone this repository and install dependencies.
```bash
git clone https://github.com/gagarinsname/simple-ets-reader
```
3. (Optional) Set up separate anaconda environment:
```bash
conda create -n ets python==3.9
```
4. Install requirements and the package itself:
```bash
cd simple-ets-reader
pip install -r requirements.txt
pip install -e .
```

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