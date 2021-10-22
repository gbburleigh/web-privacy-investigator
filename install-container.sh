#!/bin/bash
export DOCKER_BUILDKIT=0
export COMPPOSE_DOCKER_CLI_BUILD=0

docker build -t privacy-image .
