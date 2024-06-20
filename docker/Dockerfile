FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

ARG USERNAME=user
ARG PASSWORD=docker
ARG MY_UID=1000

RUN apt-get update && apt-get upgrade -y
RUN apt -y update \
	&& apt -y install apt-utils \
	&& apt -y install build-essential \
	&& apt -y install git \
	&& apt -y install libsuitesparse-dev libeigen3-dev libboost-all-dev \
	&& apt -y install libopencv-dev \
	&& apt -y install cmake \
	&& apt -y install libglew-dev \
	&& apt -y install libegl1-mesa-dev \
	&& apt -y install ffmpeg libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev \
	&& apt -y install zlib1g-dev \
	&& apt -y install sudo \
	&& apt -y install python3-opencv \
	&& apt -y install vim \
	&& apt -y install libssl-dev \
	&& apt -y install python3-pip

# add user
RUN useradd -u ${MY_UID} -m ${USERNAME} -s /bin/bash  && yes ${PASSWORD} | passwd ${USERNAME}
RUN usermod -aG sudo ${USERNAME}

# Give ssh key github
RUN mkdir /home/user/.ssh
RUN ssh-keygen -q -t rsa -N '' -f /home/user/.ssh/id_rsa

# create useful folders
RUN cd /home/user/ \
	# && mkdir -p repos/ \
	&& mkdir -p data
	
# COPY ./build.sh /home/user/code/build.sh
# COPY ./Thirdparty/ /home/user/code/Thirdparty/
# COPY ./Vocabulary/ /home/user/code/Vocabulary/
# COPY ./CMakeLists.txt /home/user/code/CMakeLists.txt
# WORKDIR /home/user/code/
# RUN ./build.sh

USER $USERNAME
ENV HOME=/home/user

COPY ./docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

WORKDIR /home/user/code/

