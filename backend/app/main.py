from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from app.core.exceptions import http_error_handler
from app.core.exceptions import http422_error_handler
from app.api.routes import router as api_router
from app.core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION, LOG_LEVEL, DEPLOYMENT_ENV
from app.core.database import create_start_app_handler, create_stop_app_handler

import logging
import sys
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # Remove any default handlers
    logger.remove()

    # Configure standard Python logging to use InterceptHandler
    # This will capture logs from libraries like Uvicorn
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    if DEPLOYMENT_ENV == "local" or DEPLOYMENT_ENV == "development":
        # Human-readable format for development, with colors
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        logger.add(sys.stderr, format=log_format, level=LOG_LEVEL, colorize=True)
    else:
        # JSON format for production
        logger.add(sys.stderr, level=LOG_LEVEL, serialize=True)

    logger.info(f"Logging configured for '{DEPLOYMENT_ENV}' environment with level: {LOG_LEVEL}")
    logger.info(f"FastAPI Project: {PROJECT_NAME}, Version: {VERSION}, Debug: {DEBUG}")


def get_application() -> FastAPI:
    setup_logging() # Call logging setup early

    application = FastAPI(title= PROJECT_NAME , debug= DEBUG , version= VERSION)
    
    # Set up event handlers for startup and shutdown
    application.add_event_handler('startup', create_start_app_handler(application))
    application.add_event_handler('shutdown', create_stop_app_handler(application))
    
    # Register custom exception handlers
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    
    # Include the API router
    application.include_router(api_router)
    
    # Set up CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    return application


app = get_application()


