import uvicorn
from core.config import settings

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        reload=True,
    )