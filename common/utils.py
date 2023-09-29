from datetime import datetime, time, timedelta
import random
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

def generate_random_datetime(start_year: int, end_year: int)->str:
    """
    Generates a random datetime string within the specified year range with weighted probabilities 
    for days of the week and time ranges.
    
    Parameters:
    - start_year (int): The start year for generating random datetime.
    - end_year (int): The end year for generating random datetime.
    
    Returns:
    - str: A random datetime string in ISO 8601 format.
    """
    # Define the days of the week with corresponding weights
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_weights = [19, 19, 19, 19, 19, 4, 1]  # Weights for each day of the week
    
    # Define the time ranges with corresponding weights
    time_ranges = [
        ('working_hours', 8, 17, 95),  # 8 am - 5 pm with 95% probability
        ('after_hours', 17, 22, 4),   # 5 pm - 10 pm with 4% probability
        ('off_hours', 22, 24, 0.5),   # 10 pm - midnight with 0.5% probability
        ('off_hours', 0, 8, 0.5),     # midnight - 8 am with 0.5% probability
    ]
    
    # Choose a random day of the week based on the given weights
    chosen_day = random.choices(days_of_week, weights=day_weights)[0]
    
    # Choose a random time range based on the given probabilities
    time_range = random.choices(time_ranges, weights=[weight for _, _, _, weight in time_ranges])[0]
    
    # Extract the details of the chosen time range
    _, start_hour, end_hour, _ = time_range
    
    # Generate a random hour, minute, and second within the chosen time range
    random_hour = random.randint(start_hour, end_hour - 1)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    
    # Generate a random year, month, and day
    random_year = random.randint(start_year, end_year)
    random_month = random.randint(1, 12)
    random_day = random.randint(1, 28) # To avoid having february the 30th and the likes
    
    # Create a base date with the generated year, month, and day
    base_date = datetime(random_year, random_month, random_day)
    
    # Calculate the number of days to shift from the base date to get the chosen day of the week
    days_shift = (days_of_week.index(chosen_day) - base_date.weekday() + 7) % 7
    
    # Generate the random date and time
    random_datetime = datetime.combine(base_date.date() + timedelta(days=days_shift), time(random_hour, random_minute, random_second))
    
    # Format the datetime object to a string in ISO 8601 format
    return random_datetime.isoformat()

def generate_random_ip()->str:
    """
    Generates a random IP address string with weighted probabilities for predefined IP addresses.
    
    Returns:
    - str: A random IP address string.
    """
    # Define the IP addresses and their corresponding probabilities
    ips = ['127.5.87.255', '127.5.87.126', 'other']  # home, office, other
    weights = [20, 78, 2]
    
    # Choose an IP address according to the given probabilities
    chosen_ip = random.choices(ips, weights)[0]

    # If 'other' is chosen, generate a random IP address
    if chosen_ip == 'other':
        chosen_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    return chosen_ip

def generate_random_request()->dict:
    """
    Generates a random request dictionary with weighted probabilities for each feature.
    
    The features include http_method, url_endpoint, user_agent, operating_system, 
    ip_address, and access_datetime.
    
    Returns:
    - dict: A dictionary containing randomly generated request features.
    """

    req = {}
    # Define generators for 4 features
    http_method_generator = [['get', 'post', 'put', 'delete'], [50, 35, 10, 5]]
    url_generator = [['/ofertas', '/pagos', '/contratos', '/dummy_route'],[30, 30, 30, 10]]
    user_agent_generator = [['safari', 'chrome', 'firefox', 'dummy_agent'], [95, 3, 1, 1]]
    operating_system_generator = [['macos', 'windows'], [95, 5]]

    # Randomly select a value for the 4 features
    req['http_method'] = random.choices(http_method_generator[0], weights=http_method_generator[1])[0]
    req['url_endpoint'] = random.choices(url_generator[0], weights=url_generator[1])[0]
    req['user_agent'] = random.choices(user_agent_generator[0], weights=user_agent_generator[1])[0]
    req['operating_system'] = random.choices(operating_system_generator[0], weights=operating_system_generator[1])[0]

    # Ip generator
    req['ip_address'] = generate_random_ip()

    # Datetime generator
    req['access_datetime'] = generate_random_datetime(2020, 2022)

    return req

