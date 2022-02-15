import datetime as dt
from decouple import config
import requests
from dateutil.relativedelta import relativedelta
from flight_data import FlightData



class FlightSearch:

    def set_dates(self):
        """This method obtains and returns date the next day and date in 6 months """
        tomorrow = dt.datetime.now().date() + dt.timedelta(days=1)
        tomorrow_date = tomorrow.strftime('%d/%m/%Y')
        return_from = tomorrow + dt.timedelta(days=14)
        return_from_date = return_from.strftime('%d/%m/%Y')
        six_months = dt.datetime.now().date() + relativedelta(months=6)
        six_months_date = six_months.strftime('%d/%m/%Y')
        return_to = six_months + dt.timedelta(days=14)
        return_to_date = return_to.strftime('%d/%m/%Y')
        return tomorrow_date, six_months_date, return_from_date, return_to_date

    def search_flights(self, lowest_prices):
        """Search for flights using tequila API"""
        tomorrow, six_months, return_from, return_to = self.set_dates()
        url = "https://tequila-api.kiwi.com/v2/search"
        headers = {
            "apiKey": config("TEQUILA_API_KEY")
        }
        object_array = []

        for city in lowest_prices:
            params = {
                "fly_from": "LON",
                "fly_to": city[0],
                "date_from": tomorrow,
                "date_to": six_months,
                "return_from": return_from,
                "return_to": return_to,
                "curr": "GBP",
                "price_to": city[1],
                "adult_hold_bag": 1,
                "asc": 1,
                "limit": 2
            }
            response = requests.get(url=url, params=params, headers=headers)
            data = response.json()
            flights = data['data']

            # create a new data object with the search result data
            flight_data = FlightData(flights)
            object_array.append(flight_data)
        return object_array


