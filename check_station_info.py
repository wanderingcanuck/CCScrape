import shelve

"""
Open shelve file containing all (as of January) names of Stations
and the Station ID's associated with them.

'BEAVERLODGE REDLOW': ['2659'],

If more than one station by the same name, the alternate station IDs are 
included in the list values.
"""

def getStationName(db):
    """
    Asks user for Station Name to get. Loops endlessly until correct
    Station Name is given.
    Uses checkStationName() function to check validity.
    """
    while True:
        station_name = raw_input("Enter Station Name (CAPITALIZED):\n> ")
        if checkStationName(station_name, db):
            break
        print "{} is not a valid Station Name. Please re-enter.".format(station_name)
    return station_name

def getStationId(station_name, db):
    """
    Gets the values (station id)for the station name.
    If more than one, asks user to confirm which station is intended.
    """
    ids = checkStationName(station_name, db)
    if len(ids) > 1:
    
        while True:
            user_id = raw_input("There are multiple Stations by the name of {name}.\nPlease choose one of the following: {station_ids}\n> ".format(name=station_name, station_ids=ids))
            if user_id in ids:
                ids = user_id
                break
            print "{} was not one of the Station Id choices. Please choose again.\n".format(user_id)
    
    return ids[0]
        
def checkStationName(station_name, db):
    """
    Checks for station name in shelving file. If found returns values,
    else returns None.
    """
    return db.get(station_name)

def stationInfo():
    """
    Main function. Opens Shelf file.
    Calls functions to ask for and confirm Station Name, Station Id.
    Returns both the station_name and station_id.
    """
    data = shelve.open('climate_database.dat')
    try:
        station_name = getStationName(data)
        station_id = getStationId(station_name, data)
    except:
        assert "Unknown Error at stationInfo(). station_name or station_id return" + \
                " invalid."
    finally:
        data.close()
    return station_name, station_id
    
def GUI_test(station_name, dirname):
    data = shelve.open('climate_database.dat')
    station_name = str(station_name)
    if checkStationName(station_name, data):
        return station_name, getStationId(station_name, data)
    else:
        exit(0)
    
if __name__ == '__main__': stationInfo()

