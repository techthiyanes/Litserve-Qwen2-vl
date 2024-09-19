# Tr OCR
Transformer OCR

## Docker build
```docker build -t barcodereader .```

### Docker run
```docker run -d --name barcodereader -p 80:80 barcodereader```

### Predict
```0.0.0.0:80/predict/model```

## Docs
```0.0.0.0:80/docs``` is provided by openApi

## Request
The image is provided in the body. ```{key:file, value: <base64 image>}```

## Actions
* Semantic Release: Triggert bei push auf main branch. Erstellt draft release
* Publish-release: Triggert bei veröffentlichtem release. Erstellt docker image und pusht auf harbor mit Versionstag

## FastApi without docker
```cd fastApi/app```
```uvicorn main:app --host 0.0.0.0 --port 80```

### Request to FastApi without docker
* ```[post] http://0.0.0.0:80/predict/model``` Post request body is of type form-data with key 'file' as base64 String
* ```[put] http://0.0.0.0:80/detect``` Put request body is of type form-data with key 'file' as File
