FROM ubuntu:20.04

RUN apt-get update && apt-get install --no-install-recommends -y \
    libgl1 \
    libgomp1 \
    python3-pip \
    python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install open3d==0.13.0
WORKDIR /simpleviz
