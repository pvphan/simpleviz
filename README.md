SimpleViz
---

Visualizing simple 3D data from files on disk should be **painless** and **portable**.
SimpleViz is a simple visualization library in a Docker container using Open3D which supports common file types.

Currently supported input types:
- .png, .bmp, .jpg [color]
- .npy [color, depth]
- .pfm [depth]


# Steps

1. Clone this repository and `cd` into it.
2. `COLOR=~/Documents/colorpath> DEPTH=<~/Documents/depthpath> make viz`

That's all!


# Possible future features

- Multiple sets of depth data, each with respective transform
- Meshes
- 'zip' mode for handling full scenes more like a blob for easier sharing

