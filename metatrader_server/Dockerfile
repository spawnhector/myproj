FROM scottyhardy/docker-wine:latest

# Install additional packages
RUN apt-get update && \
    apt-get install -y x11-apps

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    ca-certificates \
    language-pack-en \
    language-pack-zh-han* \
    locales \
    locales-all \
    wget

# GStreamer plugins
RUN apt-get update -y && \
    apt-get install -y --install-recommends \
    gstreamer1.0-libav:i386 \
    gstreamer1.0-plugins-bad:i386 \
    gstreamer1.0-plugins-base:i386 \
    gstreamer1.0-plugins-good:i386 \
    gstreamer1.0-plugins-ugly:i386 \
    gstreamer1.0-pulseaudio:i386

# Install dependencies for display scaling
RUN apt-get update -y && \
    apt-get install -y --install-recommends \
    build-essential \
    bc \
    git \
    xpra \
    xvfb \
    python3 \
    python3-pip

# Install OpenGL acceleration for display scaling
RUN pip3 install PyOpenGL==3.1.5 PyOpenGL_accelerate==3.1.5

# Install display scaling script
RUN cd /tmp && \
    git clone https://github.com/kaueraal/run_scaled.git && \
    cp /tmp/run_scaled/run_scaled /usr/local/bin/

# Install missing fonts for Chinese
RUN apt-get update -y && \
    apt-get install -y --install-recommends \
    fonts-wqy-microhei

# Install driver for Intel HD graphics
RUN apt-get -y install libgl1-mesa-glx libgl1-mesa-dri

# Set environment variables
ENV DISPLAY=host.docker.internal:0.0

# Set up X11 forwarding
RUN mkdir /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix
VOLUME /tmp/.X11-unix
ENV WINEARCH=win64 \
    WINEPREFIX=/root/.wine64
# Set entrypoint to /bin/bash
ENTRYPOINT ["/bin/bash"]
