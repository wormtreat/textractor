
# Textractor

This is a simple, mostly useless, Falcon microservice which accepts various file types and returns any text it's found in one big chunk.

It currently accepts txt, pdf and zip files. Zip file inception is a thing. Excluded file types found in zip files are disregarded.

## Usage

The service runs on port 8060. The path root produces a {status:ok}, '/upload' is the only endpoint. 
Here's an example call from a python app:

```
response = requests.post('http://localhost:8060/upload', files={"ingest": (filename, fileobj)})
```
... so, like that.

## Running

### Using Virtual Environment:
```
python3 -m venv venv
. venv/bin/activate
pip3 install -r service/requirements.txt
python3 service/app.py
```
### Using Docker:

```
docker build --no-cache --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') -t textractor/app:latest .
```

```
docker run -p 8060:8060 textractor/app
```
### Using Docker Compose:
```
docker-compose up
docker-compose down
```

## Testing and Linting

### Running locally:
#### Test:
```
pytest service/tests/*
```
#### Lint:
```
pylint service
```

### Running with Docker:
#### Test:
```
docker run textractor/app ./scripts/manage.sh test
```
or with docker-compose:
```
docker-compose run textractor ./scripts/manage.sh test
```

#### Lint:
```
docker run textractor/app ./scripts/manage.sh lint
```
or with docker-compose:
```
docker-compose run textractor ./scripts/manage.sh lint
```



