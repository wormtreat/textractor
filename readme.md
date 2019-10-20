
# Textractor

This service accepts various file types and returns any text it's found in one big chunk.

It currently accepts txt, pdf and zip files. Zip file inception is a thing. Zips can include any combination of the three.
Excluded file types found in zip files are disregarded.

## Usage

The service runs on port 8060. The path root produces a {status:ok}, '/upload' is the only endpoint. 
Here's an example call from a python app:

```
response = requests.post('http://localhost:8060/upload', files={"ingest": (filename, fileobj)})
```
... so, like that.

## Using Docker

```
docker build --no-cache --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t textractor:latest .
```

```
docker run -p 8060:8060 textractor
```
