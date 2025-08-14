# log_back

## Start app
```
uvicorn app.main:app --reload
```

## Start for local android emulator
```
uvicorn app.main:app --reload --host 192.168.0.247 --port 8001
```

## Deploy
```
// Activate venv
source .venv/bin/activate
// Start fastapi at background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60 > uvicorn.log 2>&1 &
// Start gRPC
nohup python -m app.gRPC.server > grpc_nohup.log 2>&1 &
```


## gRPC
**Generate code from proto**
```
python -m grpc_tools.protoc -I ./app/gRPC/protos/log/
```

**Run locally**
```cmd
python -m app.gRPC.server
```
**Update proto**
1. Generate pb files
```cmd 
python -m grpc_tools.protoc -I ./app/gRPC/protos --python_out=./app/gRPC/generated --grpc_python_out=./app/gRPC/generated ./app/gRPC/protos/log/common_async_log_result.proto
```
2. Change import syntax in _grpc.py
```python
from . import log_service_pb2 as log__service__pb2
```