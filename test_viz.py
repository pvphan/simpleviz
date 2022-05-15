import unittest

import numpy as np

import viz


class TestViz(unittest.TestCase):
    def setUp(self):
        self.calibrationFilePath = "calib.txt"
        self.intrinsicMatrix = np.array([
            [300, 0, 320],
            [0, 300, 240],
            [0, 0, 1],
        ], dtype=np.float32)

    def testreadCalibration(self):
        # When:
        intrinsicMatrix, baseline = viz.readCalibration(self.calibrationFilePath)

        # Then:
        self.assertEqual(intrinsicMatrix.shape, (3,3))
        self.assertIsInstance(baseline, float)

    def testintrinsicStringToMatrix(self):
        # Given:
        intrinsicString = "[7380.523 0 1100.563; 0 7380.523 974.039; 0 0 1]"

        # When:
        intrinsicMatrix = viz.intrinsicStringToMatrix(intrinsicString)

        # Then:
        self.assertEqual(intrinsicMatrix.shape, (3,3))
        self.assertTrue(np.allclose(intrinsicMatrix[2,:], (0, 0, 1)))

    def testdisparityToDepth(self):
        # Given:
        width = 640
        height = 480
        disparityMap = np.arange(width * height).reshape(height, width).astype(np.float32)
        focalLengthPx = 300
        baseline = 0.100

        # When:
        depthMap = viz.disparityToDepth(disparityMap, focalLengthPx, baseline)

        # Then:
        self.assertEqual(depthMap.shape, disparityMap.shape)


if __name__ == "__main__":
    unittest.main()
