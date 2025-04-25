from functools import wraps

from app.db.models import User, Dictionary, Word
from app.database import async_session_maker

class Repository:
    def __init__(self):
        self.session = ...
        
    def connection(method):
        @wraps(method)
        async def _wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    return await method(*args, session=session, **kwargs)
                except Exception as err:
                    await session.rollback()
                    print(f'Error: {err}')
                    raise err
        return _wrapper
                