from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


LOWEST_PRICES = [('ABV', 600), ('LOS', 600), ('PHC', 600)]

# sheets_data = DataManager()

# lowest_prices = sheets_data.get_lowest_prices()

lowest_prices = LOWEST_PRICES

flight_search = FlightSearch()
flight_objects = flight_search.search_flights(lowest_prices)
# flight_objects[0].check_return()

# Loop through each city and check if there are available flights
for city_object in flight_objects:
    flights_array = city_object.get_flight_data()
    print(flights_array)
    if len(flights_array) > 0:
        for flight in flights_array:
            notification_manager = NotificationManager()
            notification_manager.send_flight_details(flight)
