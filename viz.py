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
import itertools
import re
import os

import cv2
import numpy as np
import open3d as o3d

import pfm


def main():
    pfmFilePath = os.path.expanduser("~/Documents/vizdata/middlebury/sticks/disp0.pfm")
    colorImagePath = os.path.expanduser("~/Documents/vizdata/middlebury/sticks/im0.png")
    pointCloud = pfmToPointCloud(pfmFilePath, colorImagePath)

    box = o3d.geometry.TriangleMesh.create_box()
    o3d.visualization.draw_geometries([pointCloud])


def pfmToPointCloud(pfmFilePath, colorImagePath=""):
    disparityMap = pfm.pfmFileToDisparityMap(pfmFilePath)
    calibFilePath = f"{os.path.dirname(pfmFilePath)}/calib.txt"
    intrinsicMatrix, baseline = readCalibration(calibFilePath)
    focalLengthPx = intrinsicMatrix[0, 0]

    depthMap = disparityToDepth(disparityMap, focalLengthPx, baseline)
    pointMap = depthMapToPointMap(depthMap, intrinsicMatrix)
    points = pointMap.reshape(-1, 3)

    pointCloud = o3d.geometry.PointCloud()
    pointCloud.points = o3d.utility.Vector3dVector(points)

    if colorImagePath:
        colorImage = readColorData(colorImagePath)
        pointCloud.colors = o3d.utility.Vector3dVector(colorImage.reshape(-1, 3)/255)

    return pointCloud


def readCalibration(calibFilePath):
    parameters = {}
    with open(calibFilePath, "r") as file:
        for line in file:
            try:
                key, val = line.strip().split("=")
            except ValueError:
                break
            parameters[key] = val
    intrinsicString = parameters["cam0"]
    intrinsicMatrix = intrinsicStringToMatrix(intrinsicString)
    baselineMm = np.float32(parameters["baseline"])
    baseline = baselineMm / 1000
    return intrinsicMatrix, baseline


def intrinsicStringToMatrix(intrinsicString):
    expression = ".(\d+\.\d+)|(\d+)"
    matches = re.findall(expression, intrinsicString)
    values = [float(sorted(matchPair)[1]) for matchPair in matches]
    return np.array(values, dtype=np.float32).reshape(3,3)


def disparityToDepth(disparityMap, focalLengthPx, baseline):
    # z = fB / d
    depthMap = focalLengthPx * baseline / disparityMap
    return depthMap


def depthMapToPointMap(depthMap, intrinsicMatrix):
    # s * uv1 = K * xy1
    # ==> xy1 = s * K^-1 * uv1
    height, width = depthMap.shape[:2]
    imageCoordinates = 0.5 + np.array(list(itertools.product(range(height), range(width))))
    imageCoordinatesHom = np.hstack((imageCoordinates, np.ones((height * width, 1))))
    intrinsicMatrixInv = np.linalg.inv(intrinsicMatrix)
    normalizedPointMapArray = (intrinsicMatrixInv @ imageCoordinatesHom.T).T
    pointMapArray = depthMap.reshape(-1, 1) * normalizedPointMapArray
    pointMap = pointMapArray.reshape(height, width, 3)
    return pointMap


def readColorData(colorImagePath) -> np.array:
    colorImage = o3d.io.read_image(colorImagePath)
    return np.asarray(colorImage)


def writeVisibleDepth(pfmFilePath, outputPath):
    depthMap = pfmToPointCloud(pfmFilePath)
    depthMapNormalized = cv2.normalize(depthMap, None,
            alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    depthMapGray = (255 * depthMapNormalized).astype(np.uint8)
    depthMapJet = cv2.applyColorMap(depthMapGray, cv2.COLORMAP_JET)
    cv2.imwrite(outputPath, depthMapJet)


if __name__ == "__main__":
    main()

