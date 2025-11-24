import sys
from config import settings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'MAIN_BOT': {
            'level': settings.log_level,
            'handlers': ['console'],
            'propagate': False,
        },
        'MAIN_BACKEND': {
            'level': settings.log_level,
            'handlers': ['console'],
            'propagate': False,
        },
    },
    'root': {
        'level': settings.log_level,
        'handlers': ['console'],
    },
}