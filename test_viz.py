import unittest

import numpy as np

import viz


class TestViz(unittest.TestCase):
    def setUp(self):
        self.calibrationFilePath = "calib.txt"

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


if __name__ == "__main__":
    unittest.main()
