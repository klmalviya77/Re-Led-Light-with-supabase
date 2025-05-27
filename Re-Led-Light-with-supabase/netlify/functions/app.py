
import sys
import os

# Add the project directory to Python path
project_dir = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_dir)

# Import the Flask app
from app import app

def handler(event, context):
    """Netlify Functions handler for Flask app"""
    from werkzeug.wrappers import Request, Response
    import json
    import io
    
    # Convert Netlify event to WSGI environ
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': '',
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': '0',
        'HTTP_HOST': event.get('headers', {}).get('host', 'reled.netlify.app'),
        'wsgi.input': io.BytesIO(),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': event.get('headers', {}).get('host', 'reled.netlify.app'),
        'SERVER_PORT': '443',
    }
    
    # Handle query parameters
    if event.get('queryStringParameters'):
        query_params = []
        for key, value in event['queryStringParameters'].items():
            query_params.append(f"{key}={value}")
        environ['QUERY_STRING'] = '&'.join(query_params)
    
    # Add headers to environ
    for key, value in event.get('headers', {}).items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = 'HTTP_' + key
        environ[key] = value
    
    # Handle request body
    if event.get('body'):
        body = event['body']
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body)
        else:
            body = body.encode('utf-8')
        environ['wsgi.input'] = io.BytesIO(body)
        environ['CONTENT_LENGTH'] = str(len(body))
    
    # Create a fake start_response function
    response_data = {}
    
    def start_response(status, headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = headers
        return lambda x: None
    
    # Call the Flask app
    try:
        response_iter = app(environ, start_response)
        response_body = b''.join(response_iter)
        
        # Determine if response is binary
        is_binary = False
        content_type = ''
        for header in response_data.get('headers', []):
            if header[0].lower() == 'content-type':
                content_type = header[1]
                break
        
        # Check if content is binary
        binary_types = ['image/', 'application/pdf', 'application/zip', 'audio/', 'video/']
        is_binary = any(bt in content_type for bt in binary_types)
        
        if is_binary:
            import base64
            response_body = base64.b64encode(response_body).decode('utf-8')
        else:
            response_body = response_body.decode('utf-8')
        
        # Format response for Netlify
        status_code = int(response_data['status'].split(' ')[0])
        headers = {header[0]: header[1] for header in response_data.get('headers', [])}
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': response_body,
            'isBase64Encoded': is_binary
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}'
        }
