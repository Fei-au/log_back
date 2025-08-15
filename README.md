# log_back

## Start app
``` shell
# Now assume this is the gateway 8008, and later if we have gateway, this project use 8001
export GOOGLE_APPLICATION_CREDENTIALS=/home/usr/log_back/glass-gasket-415918-b30506c4d63f.json && uvicorn app.main:app --reload --port 8008
```

## Start for local android emulator
```
uvicorn app.main:app --reload --host 192.168.0.247 --port 8001
```

## Deploy
```shell
# 1. Activate venv
source .venv/bin/activate
# 2. Install dependencies
pip install -r requirments.txt
# 3. Set GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS=/var/www/log_back/some.json
# 4. Start fastapi at background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60 > uvicorn.log 2>&1 &
#
# Start gRPC
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