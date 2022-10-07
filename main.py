from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import requests

client_endpoint = "https://api.sheety.co/25625e1188e03ed6296be01fd8862fce/sheetycheck/sheet1"
first=input("Enter name:")
first_number=input("Enter email:")
data = { "sheet1":
             { "name": first, "email":first_number}
}

data_manager = DataManager()
#pla=DataManager.get_customer_emails()

zra = data_manager.get_customer_emails()

'''
emails1 = [row["email"] for row in zra]
print(emails1)
'''
#print(zra)
bomb=zra['sheet1']
#print(bomb)
emails=[]
names=[]
for i in bomb:
    emails.append(i['email'])
    names.append(i['name'])

if first_number in emails:
    print("Email already present")
else:

    response = requests.post(url=client_endpoint, json=data)
    #print(response.json())
#print(response.text)


#-------------------------------------------------------
import smtplib
#from notification_manager import NotificationManager
my_email="saddikutivishnu2019@iiitkottayam.ac.in"
my_password="ramahyma"

ORIGIN_CITY_IATA = "LON"


flight_search = FlightSearch()
#flight_search.check_flights('LON','PAR','02/09/2022','01/03/2023')
#notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_codes(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)
count=0
for destination_code in destinations:

    try:
        count+=1
        flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
        )
    except:
        continue

    if flight is None:
        continue
    if flight.price < destinations[destination_code]["price"]:


        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        try:
            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            NotificationManager.send_emails(emails, message, link)
        except :
            continue

#print(count)