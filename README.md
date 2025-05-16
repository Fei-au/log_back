# log_back

## Start app
```
uvicorn app:app --reload
```

## Start for local android emulator
```
uvicorn app:app --reload --host 192.168.0.17 --port 8001
```

## Deploy
```
nohup app:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60 > uvicorn.log 2>&1 &
```
