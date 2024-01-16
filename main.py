import requests
import datetime
import pandas
from dateutil.relativedelta import relativedelta
import smtplib
import os
import customeraqu

Customer_info = customeraqu.CustomerAqu()
emails = ["ashwaqal@buffalo.edu","aljanahias2016@gmail.com"]

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
Search_ENDPOINT = os.environ.get("Search_ENDPOINT")
API_KEY = os.environ.get("API_KEY")
Sheet_ENDPINT = os.environ.get("Sheet_ENDPINT")

Location_ENDPOINT = os.environ.get("Location_ENDPOINT")
message = ""
response = requests.get(url=Sheet_ENDPINT)
response.raise_for_status()
data = response.json()
now = datetime.datetime
day = now.today().date().strftime("%d" + "/" + "%m" + "/" + "%Y")
sixmonths = now.today() + relativedelta(months=+6)
date_break = sixmonths.strftime("%d" + "/" + "%m" + "/" + "%Y")
HEADER = {"apikey": API_KEY}
query = {n: data["prices"][n]["city"] for n in range(len(data["prices"]))}
prices = {}
price = {}
for n in range(len(query)):
    query2 = {
        "term": query[n]}
    response2 = requests.get(url=Location_ENDPOINT, headers=HEADER, params=query2)
    data1 = response2.json()
    prices[n] = data1["locations"][0]["code"]

ids = [data["prices"][n]["id"] for n in range(len(data["prices"]))]
data2 = []
lowest_prices = []
# Put_Sheet = os.environ.get("Put_Sheet")
# for n in range(len(prices)):
#     body = {
#         "price": {
#             "iataCode": prices[n]
#         }
#     }
    # response3 = requests.put(url=Put_Sheet+str(ids[n]),json=body)
    # response3.raise_for_status()
for n in range(len(data["prices"])):
    query = {
        "fly_from": "LON",
        "fly_to": str(data["prices"][n]["iataCode"]),
        "date_from": day,
        "date_to": date_break,
        "price_from": 0,
        "price_to": int(data["prices"][n]["lowestPrice"])
    }
    response2 = requests.get(url=Search_ENDPOINT, headers=HEADER, params=query)
    response2.raise_for_status()
    data2.append(response2.json()["data"])
for n in range(len(data2)):
    try:
        pandas.DataFrame(data2[n]).to_csv(f"flight_cheap+{n}.csv")
        data3 = pandas.read_csv(f"flight_cheap+{n}.csv")
        arrival = data3.local_arrival[n].split("T")
        departure = data3.local_departure[n].split("T")
        if data3.price[n] < int(data["prices"][n]["lowestPrice"]):
            message += f"Cheap Alert! Only ${data3.price[n]} to fly {data3.flyFrom[n]}-{data3.cityFrom[n]} to {data3.flyTo[n]}-{data3.cityTo[n]}, from {arrival[0]} to {departure[0]}\n"
    except:
        print("None found")

for i in range(len(emails)):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=emails[i],
                            msg=f"Subject:CHEAP FLIGHT ALERT\n\n{message}")
