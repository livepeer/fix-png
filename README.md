# fix-png

Tiny passthrough service that fixes truncated PNGs.

## Usage

```
docker run --rm -it -p 8765:80 livepeer/fix-png
```

Then visit [http://localhost:8765?image=https://example.com/image.png](http://localhost:8765?image=https://example.com/image.png)

## Why?

Sometimes png files are missing their last chunk. The data is all there but the file is technically invalid. This fix.
