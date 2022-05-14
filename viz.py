"""
Support visualization of the following input types:

Depth           , Color
-------------------------------------------------
.npy file (Nx3) , .npy file (Nx3)
4-channel .png  , 3-channel .{png,bmp,jpg}
.pfm            , 3-channel .{png,bmp,jpg}


TODO: arg parse:
  -c for color file,
  -d for depth file.
  use extension to automatically cast / convert data
"""
import argparse

import numpy as np
import open3d as o3d


def main():
    c = o3d.geometry.TriangleMesh.create_box()
    o3d.visualization.draw_geometries([c])


def readColorData(colorDataPath) -> np.array:
    raise NotImplementedError()


def readDepthData(depthDataPath) -> np.array:
    raise NotImplementedError()



if __name__ == "__main__":
    main()

