SimpleViz
---

Visualizing simple 3D data from files on disk should be **painless** and **portable**.
SimpleViz is a simple visualization library in a Docker container using Open3D which supports common file types.


# Steps

1. Clone this repository and `cd` into it.
2. `COLOR=~/Documents/colorpath DEPTH=~/Documents/depthpath make viz`

That's all!


# Details

Currently supported input types:
- .png, .bmp, .jpg [color]
- .npy [color, depth]
- .pfm [disparity]

If specifying a .pfm file, make sure there is a file called `calib.txt` in the same folder.
The file format should follow the Middlebury Stereo format, e.g.:

```
cam0=[7380.523 0 1100.563; 0 7380.523 974.039; 0 0 1]
cam1=[7380.523 0 1686.196; 0 7380.523 974.039; 0 0 1]
doffs=585.633
baseline=148.452
width=2864
height=2008
ndisp=300
isint=0
vmin=27
vmax=282
dyavg=0
dymax=0
```

# Possible future features

- Multiple sets of depth data, each with respective transform
- Meshes
- 'zip' mode for handling full scenes more like a blob for easier sharing

