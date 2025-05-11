from functools import wraps

from app.database import async_session_maker

class DictionaryDAO:
    def __init__(self):
        self.connect = None
    
    def connection(method):
        @wraps(method)
        async def _wrapper(self, *args, **kwargs):
            async with async_session_maker() as session:
                try:
                    self.connect = session
                    return await method(self, *args, **kwargs)
                except Exception as err:
                    await session.rollback()
                    print(f'Error: {err}')
                    raise err
        return _wrapper
