
SHELL:=/bin/bash

WORKDIR_PATH=/simpleviz
REPO_PATH:=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
IMAGE_TAG?=pvphan/simpleviz:0.1
GPU_FLAG=--device=/dev/dri:/dev/dri

RUN_FLAGS = \
	--rm \
	-it \
	${GPU_FLAG} \
	--network=host \
    -e DISPLAY=$(DISPLAY) \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
	--volume=${REPO_PATH}:${WORKDIR_PATH} \
	${IMAGE_TAG}

shell: image
	docker run ${RUN_FLAGS} bash

image:
	docker build -t ${IMAGE_TAG} .

