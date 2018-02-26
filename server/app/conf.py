settings = {
    'db_path': '/home/pi/apollo/db.json',
    'sensors_path': '/home/pi/apollo/sensors.json',
    'dt_format': '%Y-%m-%d %H:%M',
    'sensors': [{
        'mac': '00:00:00:00:00:00',
        'name': 'Guest Room'
    }],
    'display_dc': 24,
    'display_rst': 25,
    'thermometers': [
        '0000071766e4'
    ],
    'logging': {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    },
}
