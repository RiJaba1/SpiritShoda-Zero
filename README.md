# SpiritShoda-Zero
A program for processing API requests to the Shodan platform.

# Docker usage

Create custom image:

```bash
docker build -t shodan .
```

Run container:

```bash
docker run -it --rm -d -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ./datacontainer:/app/data shodan
```

> Please note you may need to execute `xhost +local:docker` before running the container.
