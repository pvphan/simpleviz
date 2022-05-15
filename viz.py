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
    #depthMap = pfmToPointCloud(pfmFilePath, colorImagePath)
    #depthMapNormalized = cv2.normalize(depthMap, None,
    #        alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    #depthMapGray = (255 * depthMapNormalized).astype(np.uint8)
    #depthMapJet = cv2.applyColorMap(depthMapGray, cv2.COLORMAP_JET)
    #outputPath = os.path.expanduser("~/Documents/vinhtest2.png")
    #cv2.imwrite(outputPath, depthMapJet)

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


def imwrite(imagePath: str, image: np.array):
    o3d.io.write_image(imagePath, o3d.geometry.Image(image))


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
    values = [float(sorted(match)[-1]) for match in matches]
    return np.array(values, dtype=np.float32).reshape(3,3)


def disparityToDepth(disparityMap, focalLengthPx, baseline):
    # z = fB / d
    depthMap = focalLengthPx * baseline / disparityMap
    return depthMap


def depthMapToPointMap(depthMap, intrinsicMatrix):
    # uv1 = K * xy1
    # ==> xy1 = K^-1 * uv1
    height, width = depthMap.shape[:2]
    imageCoordinates = np.array(list(itertools.product(range(height), range(width))))
    imageCoordinatesHom = np.hstack((imageCoordinates, np.ones((height * width, 1))))
    intrinsicMatrixInv = np.linalg.inv(intrinsicMatrix)
    normalizedPointMap = (intrinsicMatrixInv @ imageCoordinatesHom.T).T
    normalizedPointMap /= normalizedPointMap[:,2,np.newaxis]
    pointMapArray = depthMap.reshape(-1, 1) * normalizedPointMap
    pointMap = pointMapArray.reshape(height, width, 3)
    return pointMap


def readColorData(colorImagePath) -> np.array:
    colorImage = o3d.io.read_image(colorImagePath)
    return np.asarray(colorImage)


if __name__ == "__main__":
    main()

