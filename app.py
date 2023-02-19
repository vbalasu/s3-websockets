from boto3.session import Session
from chalice import Chalice

app = Chalice(app_name='s3-websockets')
app.experimental_feature_flags.update([
    'WEBSOCKETS',
])
app.websocket_api.session = Session()

api_id = '2qj9u6ewg4'
region = 'us-east-1'
stage = 'api'
endpoint = f'https://{api_id}.execute-api.{region}.amazonaws.com/{stage}'

def send_message(msg):
    import boto3
    api = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)
    connections = get_connections()
    for connection in connections:
        api.post_to_connection(Data=bytes(msg, 'utf8'), ConnectionId=connection)
    return True

@app.on_ws_connect()
def connect(event):
    print('New connection: %s' % event.connection_id)
    add_connection(event.connection_id)


@app.on_ws_message()
def message(event):
    app.websocket_api.send(event.connection_id, f'Received: {event.body}')

@app.on_s3_event(bucket='cloudmatica', events=['s3:ObjectCreated:*'])
def handle_s3_event(event):
    print(f'Received event for bucket: {event.bucket}, key: {event.key}')
    url = generate_signed_url(event.bucket, event.key)
    print(url)
    send_message(url)

def generate_signed_url(bucket, key):
    import boto3
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key})

@app.on_ws_disconnect()
def disconnect(event):
    print('%s disconnected' % event.connection_id)
    delete_connection(event.connection_id)

def add_connection(connection_id):
    import boto3
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName='connections', Item={
        'connection_id': {'S': connection_id}
    })
    return True

def get_connections():
    import boto3
    dynamodb = boto3.client('dynamodb')
    result = dynamodb.scan(TableName='connections')
    return [item['connection_id']['S'] for item in result['Items']]

def delete_connection(connection_id):
    import boto3
    dynamodb = boto3.client('dynamodb')
    dynamodb.delete_item(TableName='connections', Key={
        'connection_id': {'S': connection_id}
    })
    return True


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
