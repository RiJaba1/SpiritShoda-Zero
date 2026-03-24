# SpiritShoda-Zero
A program for processing API requests to the Shodan platform.

# Docker usage

Create custom image:

```bash
docker build -t shodan .
```

Run container (recommended for strict X11 environments, e.g. OpenSUSE):

```bash
docker run --rm -it \
	-e DISPLAY=$DISPLAY \
	-e XAUTHORITY=/tmp/.Xauthority \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $XAUTHORITY:/tmp/.Xauthority:ro \
	-v ./datacontainer:/app/data \
	shodan
```

Alternative command (may work on less restrictive setups):

```bash
docker run -it --rm -d \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v ./datacontainer:/app/data \
	shodan
```

Troubleshooting:

- If you see errors such as "Authorization required" or "could not connect to display", use the recommended command with `XAUTHORITY`.
- `xhost` may not be installed by default on some distros.
