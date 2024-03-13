from typing import List

import numpy as np

from .header import ETSHeader

class ETSVideo:
    def __init__(self, path: str):
        self.path = path
        with open(self.path, "rb") as fin:
            self.header = ETSHeader(fin)

    def _read_frame(self, index: int) -> np.ndarray:
        if index not in self.header._tile_data:
            raise ValueError(f"Can't find index {index} in tile data, must be 0 <= {index} < {self.header.n_frames}.")
        
        h, w = self.header.shape
        
        tile_params = self.header.image_address_map[index]
        offset = tile_params["offset"]
        size = tile_params["size"]

        with open(self.path, "rb") as fin:
            # search frame address memory offset
            fin.seek(offset)
            
            # read byte-size of data
            binary_data = fin.read(size)
        
        # load to numpy buffer
        img_data = np.frombuffer(binary_data, dtype=np.uint8).reshape(h, w)
        return img_data.reshape(h, w)
    
    @property
    def shape(self) -> List:
        """ get shape of sequence in as a list of type [N_FRAMES, H, W]"""
        return [self.n_frames, *self.header.shape]

    @property
    def n_frames(self) -> int:
        """ get number of frames in sequence"""
        return self.header.n_frames

    def __len__(self) -> int:
        return self.n_frames
    
    def __getitem__(self, idx: int) -> np.ndarray:
        """ Allows accessing frames as np.ndarrays by indices """
        assert 0 <= idx < self.header.n_frames, f"frame index out of range [{0}, {self.header.n_frames-1}]"
        return self._read_frame(idx)
