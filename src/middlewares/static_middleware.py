import os
from pathlib import Path

def static_middleware(app, static_dir='static'):
    """Простой middleware для статических файлов"""
    static_path = Path(__file__).parent.parent / static_dir
    
    def middleware(environ, start_response):
        path = environ['PATH_INFO']
        
        # Если запрос к статике
        if path.startswith('/static/'):
            file_path = static_path / path[8:]  # Убираем '/static/'
            
            if file_path.exists() and file_path.is_file():
                # Определяем MIME type
                if file_path.suffix == '.css':
                    content_type = 'text/css'
                elif file_path.suffix == '.js':
                    content_type = 'application/javascript'
                elif file_path.suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                    content_type = f'image/{file_path.suffix[1:]}'
                else:
                    content_type = 'text/plain'
                
                # Читаем и возвращаем файл
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                start_response('200 OK', [
                    ('Content-Type', content_type),
                    ('Content-Length', str(len(content)))
                ])
                return [content]
        
        # Если не статика - передаем основному приложению
        return app(environ, start_response)
    
    return middleware