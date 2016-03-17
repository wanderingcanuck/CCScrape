import re
from request_constants import RequestConstants

def get_station_name_and_prov(page_html):
    get_station_name_and_prov_pattern = re.compile(RequestConstants.PROV_AND_STATION, re.DOTALL | re.IGNORECASE)
    name_of_station_and_prov = get_station_name_and_prov_pattern.findall(page_html)
    return name_of_station_and_prov
            
            
def get_station_id(page_html):
    get_station_id_pattern = re.compile(RequestConstants.STATION_ID, re.DOTALL)
    station_id_list = get_station_id_pattern.findall(page_html)
    return station_id_list    
    
    
def get_number_of_stations(page_html):
    get_number_of_stations_pattern = re.compile(RequestConstants.NUMBER_OF_STATIONS, re.DOTALL | re.IGNORECASE)
    number_of_stations = get_number_of_stations_pattern.search(page_html)
            
    return int(number_of_stations.group(1))
            
def get_extra_data(page_html):
    extra_data_regex = re.compile(RequestConstants.EXTRA_DATA, re.DOTALL | re.IGNORECASE)
    extra_data = extra_data_regex.findall(page_html)
    
    return extra_data
            
def get_number_of_pages(page_html):
    list_of_page_numbers = []
    total_stations = get_number_of_stations(page_html)
    for mult_of_100 in range(2, total_stations + 1):
        if (mult_of_100 - 1) % 100 < 1:
            list_of_page_numbers.append(mult_of_100)
    return list_of_page_numbers
    
def get_years(page_html):
    get_years_pattern = re.compile(RequestConstants.NUMBER_OF_YEARS, re.DOTALL | re.IGNORECASE)
    years_list = get_years_pattern.findall(page_html)
    
    return years_list
    
def get_years_cleanup(page_html):
    get_years_first_pass_pattern = re.compile(RequestConstants.NUMBER_OF_YEARS_ROUGH, re.DOTALL | re.IGNORECASE)
    years_first_pass = get_years_first_pass_pattern.findall(page_html)
    try:
        years_cleanup = get_years(years_first_pass[0])
    except:
        return None
    return years_cleanup
    
def get_months_cleanup(page_html):
    get_months_first_pass_pattern = re.compile(RequestConstants.NUMBER_OF_MONTHS_ROUGH, re.DOTALL | re.IGNORECASE)
    months_first_pass = get_months_first_pass_pattern.findall(page_html)
    try:
        months_cleanup = get_years(months_first_pass[0])
    except:
        return None
    return months_cleanup
