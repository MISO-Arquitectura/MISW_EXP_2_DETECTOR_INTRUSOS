REQ_MAPPING = {
    'http_method': {
        'get': 1,
        'post': 2,
        'put': 3,
        'delete': 4,
        'other': 5
    },
    'url_endpoint': {
        '/ofertas': 1,
        '/pagos': 2,
        '/contratos': 3,
        'other': 4
    },
    'user_agent': {
        'safari': 1,
        'chrome': 2,
        'firefox': 3,
        'other': 4
    },
    'ip_address': {
        '127.5.87.255': 1, # home address
        '127.5.87.126': 2, # work address
        'other': 3
    },
    'operating_system': {
        'macos': 1,
        'windows': 2,
        'other': 3,
    },
    'time': {
        'work_hours': 1, # 8 am - 5 pm
        'after_hours': 2, # 5 pm - 10 pm
        'off_hours': 3, # 10 pm - 8 am
    },
    'day_of_week': {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7
    }
}