import numpy as np


def pfmFileToDisparityMap(pfmFilePath):
    fileTypesChannels = {
        "Pf": 1,
        "PF": 3,
    }
    with open(pfmFilePath, "rb") as file:
        headerLines = [file.readline().strip().decode("latin-1") for i in range(3)]
        numChannels = fileTypesChannels[headerLines[0]]
        width, height = [int(val) for val in headerLines[1].split(" ")]
        isLittleEndian = headerLines[2][0] == "-"
        scale = np.abs(float(headerLines[2]))
        endianSymbol = "<" if isLittleEndian else ">"
        bitsPerFloat = 32
        bitsPerByte = 8
        numBytesPerFloat = bitsPerFloat // bitsPerByte
        numValues = width * height * numChannels
        numBytesToRead = numValues * numBytesPerFloat
        buffer = file.read(numBytesToRead)
    finalShape = (height, width) if numChannels == 1 else (height, width, numChannels)
    flippedDisparityMap = scale * np.frombuffer(buffer, dtype=np.float32).reshape(finalShape)
    disparityMap = np.flip(flippedDisparityMap, axis=0)
    return disparityMap

