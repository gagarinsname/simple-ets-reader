from enum import Enum
import struct
from typing import BinaryIO
import warnings


class PixelTypes(Enum):
    CHAR = 1
    UCHAR = 2
    SHORT = 3
    USHORT = 4
    INT = 5
    UINT = 6
    LONG = 7
    ULONG = 8
    FLOAT = 9
    DOUBLE = 10


class ETSHeader:
    def __init__(self, file: BinaryIO):
        """
        file: binary I/O handler. Result of calling 'file = open(path_to_binary_file, "rb")'.
        """
        self.bytes_per_pixel = {"CHAR": 1, "UCHAR": 1, "SHORT": 2, "USHORT": 2}
        # read bytes from the beginning of the file
        # some comments contain source JAVA code for parsing ETS file for reference as they are not fully clear
        
        magic = struct.unpack('{}s'.format(4), file.read(4))[0]
        magic = magic.decode().strip("\x00")
        if magic[:3] != 'SIS':
            raise (f"Incorrect file: wrong magic str, expected 'SIS', got '{magic}'")
        
        unpacked = struct.unpack("iii", file.read(12))
        self.header_size = unpacked[0]
        self.version = unpacked[1]
        self.n_dimensions = unpacked[2]
        
        self.additional_header_offset = struct.unpack("q", file.read(8))[0]
        self.additional_header_size = struct.unpack("i", file.read(4))[0]
        
        file.seek(self.additional_header_offset)
        more_magic = struct.unpack('4s', file.read(4))[0].decode().strip("\x00")
        if more_magic != "ETS":
            raise ValueError(f"Incorrect file: wrong second magic str, expected 'ETS', got '{more_magic}'")
        
        # skip 4 bytes
        file.seek(32)
        self.used_chunk_offset = struct.unpack("q", file.read(8))[0]
        self.n_used_chunks = struct.unpack("i", file.read(4))[0]
        
        # read bytes from additional header address
        file.seek(self.additional_header_offset + 8)
        unpacked = struct.unpack("iiiii", file.read(20))

        self.pixel_type = unpacked[0]
        self.ms_size_c = unpacked[1]
        self.colorspace = unpacked[2]
        self.compression_type = unpacked[3]
        self.compression_quality = unpacked[4]
        
        # sanity checks, code is not fully covering all format
        if self.compression_quality != 100:
            warnings.warn(f"Got ETS image quality {self.compression_quality} < 100, perhaps lossless parsing will fail.")
        
        if self.ms_size_c != 1:
            raise ValueError(f"Only 1-channel gray images are supported, got {self.ms_size_c} channels")
        
        self.tile_x, self.tile_y, self.tile_z = struct.unpack("iii", file.read(12))
        file.seek(12 + 4 * 17, 1)
        
        pixel_type_str = PixelTypes(self.pixel_type).name
        if pixel_type_str == "ERROR":
            raise ValueError("pixel type parsing error")
        bytes_per_pixel = self.bytes_per_pixel[pixel_type_str]

        size_color = self.ms_size_c * bytes_per_pixel
        color_data = struct.unpack(f"{size_color}B", file.read(size_color))

        file.seek(4 * 10 - size_color + 4, 1)
        self.use_pyramid = struct.unpack("i", file.read(4))[0] != 0
        self.ms_rgb = self.ms_size_c > 1
        
        # read binary data from different offset
        file.seek(self.used_chunk_offset)

        # tile_offsets
        self._tile_data = {}
        for chunk in range(self.n_used_chunks):
            file.seek(4, 1)
            dimensions = self.n_dimensions
            
            t_coordinates = []
            for _ in range(dimensions):
                val = struct.unpack("i", file.read(4))[0]
                t_coordinates.append(val)
            
            tile_offset = struct.unpack("q", file.read(8))[0]
            n_bytes = struct.unpack("i", file.read(4))[0]
            file.seek(4, 1)
            
            self._tile_data[chunk] = {"offset": tile_offset, "size": n_bytes, "coordinates": t_coordinates}
    
    @property
    def shape(self):
        """Returns shape of the frames in this sequence in H x W format"""
        return (self.tile_y, self.tile_x)
    
    @property
    def h(self):
        """Returns height of the frames in this sequence"""
        return self.tile_y
    
    @property
    def w(self):
        """Returns width of the frames in this sequence"""
        return self.tile_x
    
    @property
    def n_frames(self):
        """Returns number of frames in this sequence"""
        return self.n_used_chunks
    
    @property
    def image_address_map(self):
        """Returns mapping (dict) with frame indices as keys and values - dicts with frame binary data location offsets (addresses), byte-sizes and coordinates (not used)"""
        return self._tile_data
