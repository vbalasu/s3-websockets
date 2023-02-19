# s3-websockets

Trigger a websocket message when an S3 object is created

You can use `websocat` or `wscat` to interact with a websocket endpoint, as follows:

```
wscat -c wss://2qj9u6ewg4.execute-api.us-east-1.amazonaws.com/api/
```

Simply upload any file to S3 as follows:
```
aws s3 cp hello.txt s3://cloudmatica/1d/hello.txt
```

This will trigger a websocket message to be sent to all open connections containing a signed URL to the new object.

