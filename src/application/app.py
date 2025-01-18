from fastapi import FastAPI, status
from adaptix.load_error import LoadError
from dependency.lifespan import lifespan
from starlette.responses import JSONResponse
from aiohttp.http_exceptions import HttpProcessingError

app: FastAPI = FastAPI(lifespan=lifespan)
app.add_exception_handler(
    exc_class_or_status_code=LoadError,
    handler=lambda request, exception: JSONResponse(
        {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'exception': str(exception)
        }
    )
)
app.add_exception_handler(
    exc_class_or_status_code=HttpProcessingError,
    handler=lambda request, exception: JSONResponse(
        {
            'status_code': request.status_code,
            'exception': str(exception)
        }
    )
)
app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=lambda request, exception: JSONResponse(
        {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'exception': str(exception)
        }
    )
)