from datetime import datetime, time, timedelta
from .constants import REQ_MAPPING

def map_datetime(datetime_str, mapping)->tuple:
    """
    Maps the input datetime string to corresponding time and day_of_week categories.
    
    Parameters:
    - datetime_str (str): The datetime string in ISO 8601 format to be mapped.
    - mapping (dict): The mapping dictionary containing time and day_of_week categories.
    
    Returns:
    - tuple: A tuple containing mapped time and mapped day_of_week.
    """
    # Parse the datetime string to a datetime object
    dt = datetime.fromisoformat(datetime_str)
    
    # Extract the time and day of the week
    t = dt.time()
    day_of_week = dt.strftime('%A').lower()
    
    # Map the time to the corresponding category
    if time(8, 0) <= t <= time(17, 0):
        mapped_time = mapping['time']['work_hours']
    elif time(17, 0) < t <= time(22, 0):
        mapped_time = mapping['time']['after_hours']
    else:
        mapped_time = mapping['time']['off_hours']
    
    # Map the day of the week to the corresponding category
    mapped_day_of_week = mapping['day_of_week'][day_of_week]
    
    return mapped_time, mapped_day_of_week

def get_request_mapping(req: dict)->dict:
    """
    Maps the features of the input request dictionary to corresponding categories using a predefined mapping.
    
    Parameters:
    - req (dict): The input request dictionary containing features to be mapped.
    
    Returns:
    - dict: A dictionary containing the mapped features.
    """
    mapped_dict = {}
    # Loop over the req dict
    for feature, value in req.items():
        if feature != 'access_datetime':
            mapped_feature = REQ_MAPPING[feature].get(value) if REQ_MAPPING[feature].get(value) is not None else REQ_MAPPING[feature]['other']
            mapped_dict[feature] = mapped_feature
        else:
            mapped_time, mapped_day_of_week = map_datetime(value, REQ_MAPPING)
            mapped_dict['time'] = mapped_time
            mapped_dict['day_of_week'] = mapped_day_of_week
    return mapped_dict