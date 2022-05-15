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
import re
import os

import numpy as np
import open3d as o3d

import pfm


def main():
    colorImagePath = os.path.expanduser("~/Documents/vizdata/middlebury/sticks/im0.png")
    colorImage = readColorData(colorImagePath)
    colors = colorImage.reshape(-1, 3)

    pfmFilePath = os.path.expanduser("~/Documents/vizdata/middlebury/sticks/disp1.pfm")
    pointCloud = pfmToPointCloud(pfmFilePath)

    c = o3d.geometry.TriangleMesh.create_box()
    o3d.visualization.draw_geometries([c])


def pfmToPointCloud(pfmFilePath):
    disparityMap = pfm.pfmFileToDisparityMap(pfmFilePath)
    calibFilePath = f"{os.path.dirname(pfmFilePath)}/calib.txt"
    intrinsicMatrix, baseline = readCalibration(calibFilePath)
    focalLengthPx = intrinsicMatrix[0, 0]

    points = disparityToDepth(disparityMap, focalLengthPx, baseline)

    pointCloud = o3d.geometry.PointCloud()
    pointCloud.points = o3d.utility.Vector3dVector(points)
    return pointCloud


def readCalibration(calibFilePath):
    parameters = {}
    with open(calibFilePath, "r") as f:
        for line in f:
            try:
                key, val = line.strip().split("=")
            except ValueError:
                break
            parameters[key] = val
    intrinsicString = parameters["cam0"]
    intrinsicMatrix = intrinsicStringToMatrix(intrinsicString)
    baselineMm = float(parameters["baseline"])
    baseline = baselineMm / 1000
    return intrinsicMatrix, baseline


def intrinsicStringToMatrix(intrinsicString):
    expression = ".(\d+\.\d+)|(\d+)"
    matches = re.findall(expression, intrinsicString)
    values = [float(sorted(match)[-1]) for match in matches]
    return np.array(values, dtype=np.float32).reshape(3,3)


def disparityToDepth(disparityMap, focalLengthPx, baseline):
    # z = fB / d
    z = focalLengthPx * baseline / disparityMap
    return z


def readColorData(colorDataPath) -> o3d.cpu.pybind.geometry.Image:
    colorImage = o3d.io.read_image(colorDataPath)
    return colorImage


def readDepthData(depthDataPath) -> np.array:
    raise NotImplementedError()



if __name__ == "__main__":
    main()

