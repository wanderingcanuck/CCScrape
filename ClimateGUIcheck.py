import shelve

"""
Open shelve file containing all (as of January) names of Stations
and the Station ID's associated with them.

'BEAVERLODGE REDLOW': ['2659'],

If more than one station by the same name, the alternate station IDs are 
included in the list values.
"""
    
def getStationId(station_name):
    """
    Gets the values (station id)for the station name.
    If more than one, asks user to confirm which station is intended.
    """
    db = getDatabase()
    ids = checkStationName(station_name, db)
    db.close()
    if len(ids) > 1:
        return False, ids
    return True, ids
        
def checkStationName(station_name):
    """
    Checks for station name in shelving file. If found returns values,
    else returns None.
    """
    db = getDatabase()
    station_check = db.get(station_name)
    db.close()
    return station_check
    
def getDatabase():
    return shelve.open('climate_database.dat')
    
if __name__ == '__main__': stationInfo()
