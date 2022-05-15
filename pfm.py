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
        isBigEndian = headerLines[2][0] != "-"
        scale = np.abs(float(headerLines[2]))
        endianSymbol = ">" if isBigEndian else "<"
        bitsPerFloat = 32
        bitsPerByte = 8
        numBytesPerFloat = bitsPerFloat // bitsPerByte
        numValues = width * height * numChannels
        numBytesToRead = numValues * numBytesPerFloat
        buffer = file.read(numBytesToRead)
    finalShape = (height, width) if numChannels == 1 else (height, width, numChannels)
    disparityMap = scale * np.frombuffer(buffer, dtype=np.float32).reshape(finalShape)
    return np.flip(disparityMap, axis=0)

