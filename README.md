# log_back

## Start app
```
uvicorn app:app --reload
```

## Deploy
```
nohup app:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60 > uvicorn.log 2>&1 &
```
