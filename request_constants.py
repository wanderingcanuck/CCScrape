# request patterns

class RequestConstants(): # keeps a collection of all the CONSTANTS such as Regex expressions
    
    PROV_AND_STATION = r'station\s+wordwrap">(.*?)\s+<\/div>\s+<.+?>(AB|BC|NS|NB|NL|QC|SK|ON|YT|NT|PE|NU|MB)'
    STATION_ID = r'"StationID"\svalue="(\d+)"'
    NUMBER_OF_STATIONS = r'<p>(\d+?)\slocations\smatch'
    EXTRA_DATA = r'name="(hlyRange|dlyRange|mlyRange|StationID|Prov|)"\svalue="(.*?)"'
    NUMBER_OF_YEARS = r'<option\svalue=.*?>(.*?)<'
    NUMBER_OF_YEARS_ROUGH = r'id="Year1".*?>.*?<\/select>'
    NUMBER_OF_MONTHS_ROUGH = r'id="Month1".*?>.*?<\/select>'
