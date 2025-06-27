# log_back

## Start app
```
uvicorn app.main:app --reload
```

## Start for local android emulator
```
uvicorn app.main:app --reload --host 192.168.0.17 --port 8001
```

## Deploy
```
// Activate venv
source .venv/bin/activate
// Start fastapi at background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60 > uvicorn.log 2>&1 &
// Start gRPC
nohup python -m app.gRPC.grpc_server > grpc_nohup.log 2>&1 &
```


## gRPC
**Run locally**
```cmd
python -m app.gRPC.grpc_server
```
**Update proto**
1. Generate pb files
```cmd 
python -m grpc_tools.protoc -I ./app/gRPC --python_out=./app/gRPC --grpc_python_out=./app/gRPC ./app/gRPC/log_service.proto
```
2. Change import syntax in _grpc.py
```python
from . import log_service_pb2 as log__service__pb2
```