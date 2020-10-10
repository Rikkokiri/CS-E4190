# The base image must be ubuntu:latest.
FROM ubuntu:latest

# Solve entering timezone: https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# It specifies /application as the working directory.
WORKDIR /application

# It defines the PYTHON_VERSION argument only if it supports build-time arguments.
ARG PYTHON_VERSION=2.7

# Make sure that you have all necessary software installed in the container.
# The step that builds the python package relies on a C / C++ compiler (with gcc recommended) to build native libraries
# that need to be included in the wheel.
# -------------------------------------------------------------
# Install dependencies 	pip install -r requirements.txt
# Syntax check 	python -m compile_all .
# Linting 	pyLint
# Unit testing 	pytest
# Build wheel package 	pip, C / C++ development tools, python-dev

# Install both Python versions
RUN if [ "$PYTHON_VERSION" = "2.7" ]; then \
		apt-get update && apt-get install -y \
		curl \
		python2.7 \
		python-setuptools \
		python-dev \
		pylint \
		gcc \
		g++ \
		&& curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py \
		&& python2 get-pip.py \
		&& pip install pytest \
		&& pip install wheel; \
	else \
		apt-get update && apt-get install -y \
		curl \
		python3.8 \
		python3-setuptools \
		python3-pip \
		pylint \
		python3-dev \
		gcc \
		g++ \
		&& pip3 install pytest \
		&& pip3 install wheel; \
	fi
