# parsing the website for csv files and other data
import call_climate_canada
import logging

logging.basicConfig(filename='ABEE_ADGM_DEBUG_LOG.txt', level=logging.DEBUG, format=' %(asctime)s = %(levelname)s - %(message)s')
logging.debug('')
logging.debug('Start of Program')

logging.debug('Creating instance of CallClimateCanada')
new_html = call_climate_canada.CallClimateCanada('')
logging.debug('Created {}' .format(new_html))

abee_adgm_html = new_html.get_html('http://climate.weather.gc.ca/climateData/monthlydata_e.html?StationID=' + '32232')
logging.debug('Retrieved HTML from {}' .format('http://climate.weather.gc.ca/climateData/monthlydata_e.html?StationID=' + '32232'))

with open('ABEE_ADGM_MONTHLY.txt', 'w') as f:
    logging.debug('Writing to file...')
    f.write(abee_adgm_html)
    logging.debug('Finished writing to file...')