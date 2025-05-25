import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from main import app

def handler(event, context):
    """Netlify Functions handler for Flask app"""
    from werkzeug.wrappers import Request, Response
    import json
    
    # Convert Netlify event to WSGI environ
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': str(len(event.get('body', ''))),
        'HTTP_HOST': event.get('headers', {}).get('host', 'localhost'),
        'wsgi.input': None,
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
    }
    
    # Add headers to environ
    for key, value in event.get('headers', {}).items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = 'HTTP_' + key
        environ[key] = value
    
    # Handle request body
    if event.get('body'):
        import io
        environ['wsgi.input'] = io.StringIO(event['body'])
    
    # Create a fake start_response function
    response_data = {}
    
    def start_response(status, headers, exc_info=None):
        response_data['status'] = status
        response_data['headers'] = headers
        return lambda x: None
    
    # Call the Flask app
    try:
        response_iter = app(environ, start_response)
        response_body = b''.join(response_iter).decode('utf-8')
        
        # Format response for Netlify
        status_code = int(response_data['status'].split(' ')[0])
        headers = {header[0]: header[1] for header in response_data.get('headers', [])}
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': response_body
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}'
        }