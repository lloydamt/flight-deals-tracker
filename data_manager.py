import requests
from decouple import config

# 1.    Get the cities from google sheet and store them in a list
# 2.    Loop through each item in the list and obtain iata codes through kiwi API
# 3.    Attach id to iata codes
# 4.    Using put method, write the iata codes to the google sheets file, using the row id to match the codes

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._cities = self.get_cities()
        self._iata = self.get_codes(self._cities)
        self.write_to_sheet(self._iata)

    def get_cities(self):
        url = f'https://api.sheety.co/{config("SHEET_ID")}/flightDeals2/prices'
        headers = {
            'Authorization': f"Basic {config('SHEET_KEY')}"
        }
        response = requests.get(url=url, headers=headers)
        data = response.json()
        cities = [(city['id'], city['city']) for city in data['prices']]
        return cities

    def get_lowest_prices(self):
        url = f'https://api.sheety.co/{config("SHEET_ID")}/flightDeals2/prices'
        headers = {
            'Authorization': f"Basic {config('SHEET_KEY')}"
        }
        response = requests.get(url=url, headers=headers)
        data = response.json()
        lowest_prices = [(city['iataCode'], city['lowestPrice']) for city in data['prices']]
        return lowest_prices

    def get_codes(self, cities):
        url = 'https://tequila-api.kiwi.com/locations/query'

        headers = {
            "apiKey": config("TEQUILA_API_KEY")
        }

        iata = []

        for city in cities:
            params = {
                "term": city[1],
                "locale": "en-US",
                "location_types": "airport",
                "limit": 1,
                "active_only": "true"
            }
            response = requests.get(url=url, params=params, headers=headers)
            data = response.json()
            city_iata = data['locations'][0]['city']['code']
            iata.append((city[0], city_iata))
        return iata

    def write_to_sheet(self, iata_codes):
        for city in iata_codes:
            url = f"https://api.sheety.co/{config('SHEET_ID')}/flightDeals2/prices/{city[0]}"
            body = {
                "price": {
                    "iataCode": city[1]
                }
            }
            headers = {
                'Authorization': f"Basic {config('SHEET_KEY')}"
            }
            requests.put(url=url, json=body, headers=headers)

