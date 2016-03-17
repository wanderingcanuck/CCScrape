import urllib
import re
import climate_parsing
import shelve

class CallClimateCanada(): # handles the changing of links, calling of webpages, etc.

        def __init__(self, page_link):
            self.page_link = page_link
            self.station_name_and_prov = []
            self.station_id = []
            self.list_of_page_numbers = []
            self.extra_data = []
            self.data_file = shelve.open('climate_data.dat')

        
        def get_html(self, link):
        
            try:
                print "Opening link"
                print "{}" .format(link)
                self.connection = urllib.urlopen(link, 'r')
                self.page_html = self.connection.read()
                self.connection.close()
            except:
                print "There was an error opening and reading {}." .format(self.page_link)
                print "Now quitting.\nGoodbye!"
            
            return self.page_html

        
        def get_search_page_info(self, html):

            station_name = climate_parsing.get_station_name_and_prov(html)
            print "Parsing Station Name"
            station_id_number = climate_parsing.get_station_id(html)
            print "Parsing Station Id"
            extra_data_parsed = climate_parsing.get_extra_data(html)
            print "Parsing extra data."
            
            for item in station_name:
                self.station_name_and_prov.append(item)
            for item in station_id_number:
                self.station_id.append(item)
            self.tuples_list = []
            for item in extra_data_parsed:
                if item[0] != 'Prov':
                    self.tuples_list.append(item[1])
                elif item[0] == 'Prov':
                    self.tuples_list.append(item[1])
                    self.extra_data.append(self.tuples_list)
                    self.tuples_list = []
                else:
                    print "ERROR"
                    print item
                    exit()

            print "Appended items"
            
        
        # def call_websites(self):
        
            # """
            # The website seems to double up on the last entry starting with the second page.
            # Will need to clean list up afterwards.
            # """
            
            # first_html_page = self.get_html(self.page_link)
            # self.list_of_page_numbers = climate_parsing.get_number_of_pages(first_html_page)
            # self.get_search_page_info(first_html_page)
            
            # if len(self.list_of_page_numbers) > 0:
                
                # for num in self.list_of_page_numbers:
                    # print "Changing Pages"
                    # try:
                        # self.next_page = self.page_link + '&startRow=' + str(num)
                        
                        # self.get_search_page_info(self.get_html(self.next_page))
                    # except:
                        # print "Something went wrong on page {} to {}" .format(num, num + 100)
                       
            # with open('test_the_climate.txt', 'w') as f:
                
                # new_list = zip(self.station_name_and_prov, self.extra_data)
                
                # print "Zipping Files"
                # for item in new_list:
                    
                    # f.write(str(item) + '\n' )
                    
            # print "FINISHED! ALL DONE"
            # print len(new_list)

        def call_websites(self):
        
            """
            The website seems to double up on the last entry starting with the second page.
            Will need to clean list up afterwards.
            """
            
            first_html_page = self.get_html(self.page_link)
            self.list_of_page_numbers = climate_parsing.get_number_of_pages(first_html_page)
            self.get_search_page_info(first_html_page)

            if len(self.list_of_page_numbers) > 0:
                
                for num in self.list_of_page_numbers:
                    print "Changing Pages"
                    try:
                        self.next_page = self.page_link + '&startRow=' + str(num)
                        
                        self.get_search_page_info(self.get_html(self.next_page))
                    except:
                        print "Something went wrong on page {} to {}" .format(num, num + 100)
                        
            
            # Test code for separating the Station Name from the Province for zipping
            
            self.station_name = [item[0] for item in self.station_name_and_prov]
                       
            new_list = zip(self.station_name, self.extra_data)
                       
            
                       
            with open('test_the_climate.txt', 'w') as f:
                
                
                
                print "Zipping Files"
                for item in new_list:
                    self.data_file[item[1][3]] = item
                    f.write(str(item) + '\n' )
                    
            self.data_file.close()
            print "FINISHED! ALL DONE"
            print len(new_list)

def Main():
    pass
    
    # ('ACADIA FOREST EXP ST', [('hlyRange', '|'), ('dlyRange', '1955-01-01|2010-04-27'), ('mlyRange', '1955-01-01|2006-02-01'), ('StationID', '6106'), ('Prov', 'NB')])
            
if __name__ == '__main__': Main()
