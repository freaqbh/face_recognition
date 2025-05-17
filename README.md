# Face Reconition with Deepface

pake firebase untuk store picture, real time pake websocket go untuk ngambil per frame lalu cocokan


setup python
```
python -m venv venv
```

```
pip install -r requirements.txt
```

```
python app.py
```

setup golang
```
go mod init websocket
```

```
go get github.com/gorilla/websocket
```

```
go mod tidy
```

```
go run main.go
```
