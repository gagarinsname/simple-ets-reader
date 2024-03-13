import argparse
import os

from matplotlib import pyplot as plt

from ets_reader import ETSVideo

def parse_args():    
    parser = argparse.ArgumentParser(description="Run demo of grayscale ETS reader")
    parser.add_argument("-i", "--input", required=True, type=str, help="path to input file with .ets format")
    parser.add_argument("--index", default=0, type=int, help="index of a frame of .ets file to visualize")
    return parser.parse_args()

if __name__ == "__main__":
    # read command line arguments
    args = parse_args()

    # sanity check
    assert os.path.exists(args.input), f"file not found: {args.input}"
    file_path = args.input
    frame_index = args.index

    # read ETS frame sequence header and frame locations in memory
    sequence = ETSVideo(file_path)
    n_frames = len(sequence)
    print(f"loaded ETS sequence with {n_frames} frames")
    
    # get frame sequence metadata
    num_frames, frame_h, frame_w = sequence.shape
    
    # get a certain frame
    img = sequence[frame_index]
    
    # visualize using matplotlib
    fig = plt.figure(figsize=(15, 10))
    ax = plt.imshow(img, cmap="gray")
    plt.title(f"frame no: {frame_index} of {num_frames} || size: {frame_h} x {frame_w}")
    plt.show()
    
    exit(0)