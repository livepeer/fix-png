.PHONY: all
all: docker

.PHONY: docker
push:
	docker buildx build --platform linux/amd64,linux/arm64 -t livepeer/fix-png --push .
