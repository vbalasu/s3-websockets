import app

def test_add_connection():
    result = app.add_connection('testing')
    assert result is True

def test_get_connections():
    result = app.get_connections()
    assert result == ['testing']

def test_delete_connection():
    result = app.delete_connection('testing')
    assert result is True

def test_generate_signed_url():
    result = app.generate_signed_url('cloudmatica', '1d/hello.txt')
    assert 's3' in result

def test_send_message():
    result = app.send_message('TEST MESSAGE')
    assert result is True