
SHELL:=/bin/bash

WORKDIR_PATH=/simpleviz
REPO_PATH:=$(dir $(abspath $(firstword $(MAKEFILE_LIST))))
# TODO: mount color and depth files as read only volume mounts
#COLOR_DIR_PATH:=$(dir $(abspath $(firstword $(COLOR))))
#DEPTH_DIR_PATH:=$(dir $(abspath $(firstword $(DEPTH))))
# TODO: support comma separated input paths
IMAGE_TAG?=pvphan/simpleviz:0.1
GPU_FLAG=--device=/dev/dri:/dev/dri
#GPU_FLAG=--gpus 'all,"capabilities=compute,utility,graphics"'

NVIDIA_SMI_RESULT:=$(shell which nvidia-smi)
ifeq ($(NVIDIA_SMI_RESULT),)
	GPU_FLAG=--device=/dev/dri:/dev/dri
else
	GPU_FLAG=--gpus 'all,"capabilities=compute,utility,graphics"'
endif

RUN_FLAGS = \
	--rm \
	-it \
	${GPU_FLAG} \
    -e DISPLAY=$(DISPLAY) \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
	--volume=${REPO_PATH}:${WORKDIR_PATH} \
	${IMAGE_TAG}

viz: image
	docker run ${RUN_FLAGS} python viz.py -c $(COLOR) -d $(DEPTH)

shell: image
	docker run ${RUN_FLAGS} bash

image:
	docker build -t ${IMAGE_TAG} .

