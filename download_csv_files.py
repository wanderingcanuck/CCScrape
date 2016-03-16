import urllib
import call_climate_canada
from climate_parsing import get_years, get_years_cleanup, get_months_cleanup
import logging
import os
import check_station_info as station_info

def Main(dirname, station_name=None, station_id=None):

    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Start Of Program')
    # station_name, station_id = station_info.stationInfo()
     
    if not station_id or not station_name:
        print """Station Name or Station ID was not entered. This is a requirement to proceed.\n
        Please note that the CLIMATE ID is not the same as the STATION ID."""
        print "Please run the program again."
        print "Now EXITTING."
        exit()
        
    """
    Creates an URL using the Station ID, one URL for each (monthly, daily, hourly).
    """
    timeframe_urls = {
                        'monthly_url':'http://climate.weather.gc.ca/climateData/monthlydata_e.html?timeframe=3&StationID=' + station_id,
                        'daily_url':'http://climate.weather.gc.ca/climateData/dailydata_e.html?timeframe=2&StationID=' + station_id,
                        'hourly_url':'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&StationID=' + station_id
                      }

    """
    Creates an Instance for each timeframe ('monthly_url, daily_url, hourly_url').
    Could be removed and added to the corresponding download functions.
    """                  
    monthly_html = call_climate_canada.CallClimateCanada(timeframe_urls['monthly_url'])
    daily_html = call_climate_canada.CallClimateCanada(timeframe_urls['daily_url'])
    hourly_html = call_climate_canada.CallClimateCanada(timeframe_urls['hourly_url'])

    # Don't need this dictionary in the program, just good to have on hand
    month_values = {                        
                    'January':'1',
                    'February':'2',
                    'March':'3',
                    'April':'4',
                    'May':'5',
                    'June':'6',
                    'July':'7',
                    'August':'8',
                    'September':'9',
                    'October':'10',
                    'November':'11',
                    'December':'12'
                    }

    # Don't need this dictionary in the program, just good to have on hand                
    timeframe_keys = {
                      '1':'hourly',
                      '2':'daily',
                      '3':'monthly'
                      }

    # To download the monthly data
    # parses the monthly webpage and calls the download_csv function with the information
    """
    - html = calls get_html to return the html of monthly web page
    - years = calls get_years to parse webpage for all years station was active
    - If years are empty (none found), print statement and exit function
    - There is guarunteed only to be ONE csv file to download for Monthly,
      so years = years[-1] grabs a year and calls download_csv(station_id, timeframe, year_to_download)
    """
    def download_monthly_csv(link): 
        
        logging.debug('Start Of Download_Monthly_CSV\n{}' .format(link))
        
        html = monthly_html.get_html(link)
        years = get_years(html)
        if years == None or years == []:
            logging.debug("No Monthly Data found for {}." .format(station_name))
            return
        years = years[-1]
        logging.debug('Calling download_csv for year {}' .format(years))
        download_csv(station_id, '3', Year=years)
        logging.debug('Download for Monthly is successful!')
        return

    """
    - html = calls get_html to return the html of hourly web page
    - years = call get_years_cleanup to grab the years from the html. Requires
      extra cleanup (two seperate Regex expressions) to parse through and get
      all the years.
    - If years are empty (none found), print statement and exit function
    - Otherwise call download_csv for EACH year in list of years
    """ 
    def download_daily_csv(link):

        logging.debug('Start Of Download_Daily_CSV\n{}' .format(link))
        
        html = daily_html.get_html(link)
        years = get_years_cleanup(html)
        if years == None or years == []:
            logging.debug("No Daily Data found for {}." .format(station_name))
            return
        logging.debug('Years: {}' .format(years))
        for year in years:
            logging.debug('year')
            download_csv(station_id, '2', Year=year)
            logging.debug('Download for Daily for {}' .format(year))
        return
    """
    - html = calls get_html to return the html of hourly web page
    - years = call get_years_cleanup to grab the years from the html. Requires
      extra cleanup (two seperate Regex expressions) to parse through and get
      all the years.
    - If years are empty (none found), print statement and exit function
    - Otherwise call download_csv for EACH year in list of years
    - THEN get each month for each year (not guarunteed to have all months for
      each year.)
    """ 
    def download_hourly_csv(link):

        logging.debug('Start Of Download_Hourly_CSV\n{}' .format(link))
        
        html = hourly_html.get_html(link)
        years = get_years_cleanup(html)
        if years == None or years == []:
            logging.debug("No Hourly Data found for {}." .format(station_name))
            return
        logging.debug('Years: {}' .format(years))
        for year in years:
            logging.debug('year: {}' .format(year))
            link_for_year = timeframe_urls['hourly_url'] + '&Year={}' .format(year)
            html_for_year = hourly_html.get_html(link_for_year)
            list_of_months = get_months_cleanup(html_for_year)
            logging.debug('months: {}' .format(list_of_months))
            for month in list_of_months:
                download_csv(station_id, '1', year, month_values[month])

    """
    - urlencode all CGI parameters and add them to the main url for the webpage
      to download information from.
      The parameters(payload) default to the normal unless overridden by the 
      functions above.
    - Opens the new url (download_url + param_encode), reads and saves html.
    - create filename via appropriate syntax
    - If filepath does not exist, create new folder for files.
    - write to file, line by line, for each time download_csv is called.
    """            
    def download_csv(stationID, timeframe, Year='2016', Month='1', Day='1' ,format='csv', submit='Download Data'):

        payload = {                              # form paramaters for submitting request for .csv file
                   'format':format,
                   'stationID':stationID, 
                   'Year':Year, 
                   'Month':Month, 
                   'Day':Day, 
                   'timeframe':timeframe, 
                   'submit':submit
                   }
                   
        param_encode = urllib.urlencode(payload) # example: format=csv&Year=1975&submit=Download+Data&Month=1&stationID=628&timeframe=3&Day=1
        download_url = 'http://climate.weather.gc.ca/climateData/bulkdata_e.html?'
        
        response = urllib.urlopen(download_url + param_encode, 'r')
        response_text = response.read()
        response_text_split = response_text.split('\n')
        
        filename = station_name + '_' + timeframe_keys[payload['timeframe']] + '_' + payload['Year'] + '_' + payload['Month'] + '_' + payload['Day'] + '.' + payload['format'] # filename for new .csv file
        file_path = os.path.join(dirname, station_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        with open(os.path.join(file_path, filename), 'w') as f:
            for line in response_text_split:
                f.write(line + '\n')   
        return
    
    # call functions for each timeframe.
    download_monthly_csv(timeframe_urls['monthly_url'])
    download_daily_csv(timeframe_urls['daily_url'])
    download_hourly_csv(timeframe_urls['hourly_url'])

if __name__ == '__main__': Main(dirname, station_name, station_id)
