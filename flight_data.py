import requests
from decouple import config


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, data):
        self.flight_data = data

    def get_flight_data(self):
        return self.flight_data