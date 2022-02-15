import smtplib
from decouple import config
from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.account_sid = config('TWILIO_ACCOUNT_SID')
        self.auth_token = config('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid, self.auth_token)

    def send_flight_details(self, flight_info):
        price = flight_info['price']
        city_from = flight_info['cityFrom']
        airport_from_code = flight_info['flyFrom']
        city_to = flight_info['cityTo']
        airport_to_code = flight_info['flyTo']
        departure_date = flight_info['route'][0]['local_departure'][:10]
        return_date = flight_info['route'][1]['local_departure'][:10]
        booking_link = flight_info['deep_link']
        from_email = config('FROM_EMAIL')
        password = config('PASSWORD')
        to_email = config('TO_EMAIL')


        # message = self.client.messages \
        #     .create(
        #     body=f"Low price alert! Only £{price} to fly from {city_from}-{airport_from_code}"
        #          f" to {city_to}-{airport_to_code} , "
        #          f"from {departure_date} to {return_date}\n"
        #          f"Book: {booking_link}",
        #     from_=f'{config("TWILIO_NUM")}',
        #     to=f'{config("PHONE")}'
        # )

        # Send Email with flight details
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=from_email, password=password)
            connection.sendmail(from_addr=from_email, to_addrs=to_email,
                                msg=f'Subject: Low price alert!\n\n Only {price}'
                                    f' to fly from {city_from}-{airport_from_code} to {city_to}-{airport_to_code},'
                                    f' from {departure_date} to {return_date}\n'
                                    f'Book: {booking_link}'
                                )
