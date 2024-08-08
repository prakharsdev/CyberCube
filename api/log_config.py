import logging
import logging.config

def setup_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'level': 'INFO',
                'filename': 'api.log',
                'mode': 'a',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            },
            'my_module': {  # if you want to have a custom logger for a specific module
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }

    logging.config.dictConfig(logging_config)

# Call this function in your main application file to initialize logging
setup_logging()
