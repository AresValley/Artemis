import logging
import logging.config
from constants import __BASE_FOLDER__
import os.path

"""Import the module to initialize the logging configuration"""

_LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'general': {
            'format': '%(asctime)s::%(levelname)s::%(module)s::%(funcName)s::%(message)s',
            'datefmt': '%d/%m/%Y %I:%M:%S %p'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'general',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'filename': os.path.join(__BASE_FOLDER__, 'info.log'),
            'mode': 'w',
            'encoding': 'utf8',
            'formatter': 'general'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    },
    'loggers': {
        'root.sublogger': {
            'propagate': False,
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}

logging.config.dictConfig(_LOGGING_CONFIG)
