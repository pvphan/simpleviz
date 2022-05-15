import os
import struct

import numpy as np


def pfmFileToDisparityMap(pfmFilePath):
    fileTypesChannels = {
        "Pf": 1,
        "PF": 3,
    }
    with open(pfmFilePath, "rb") as f:
        headerLines = [f.readline().strip().decode("latin-1") for i in range(3)]
        numChannels = fileTypesChannels[headerLines[0]]
        width, height = [int(val) for val in headerLines[1].split(" ")]
        isBigEndian = headerLines[2][0] == "-"
        endianSymbol = ">" if isBigEndian else "<"
        numBytesPerFloat = 4
        numValues = width * height * numChannels
        buffer = f.read(numValues * numBytesPerFloat)
    finalShape = (height, width) if numChannels == 1 else (height, width, numChannels)
    parsedData = np.frombuffer(buffer, dtype=np.float32).reshape(finalShape)
    return parsedData



if __name__ == "__main__":
    main()

