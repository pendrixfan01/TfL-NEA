# import requests

# def fetch_bus_arrival_times(bus_stop_code, app_id, app_key):
#     """
#     Fetches the bus arrival times for a given bus stop from the TfL API.

#     :param bus_stop_code: The unique code for the bus stop (stopPointId or naptanId).
#     :param app_id: TfL API application ID.
#     :param app_key: TfL API application key.
#     :return: List of bus arrival times.
#     """
#     base_url = f"https://api.tfl.gov.uk/StopPoint/{bus_stop_code}/Arrivals"
#     params = {
#         "app_id": app_id,
#         "app_key": app_key
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  # Raise HTTPError for bad responses
#         arrivals = response.json()

#         # Sort arrivals by expected arrival time
#         sorted_arrivals = sorted(arrivals, key=lambda x: x["timeToStation"])
#         arrival_data = [
#             {
#                 "lineName": item["lineName"],
#                 "destinationName": item["destinationName"],
#                 "timeToStation": item["timeToStation"] // 60  # Convert seconds to minutes
#             }
#             for item in sorted_arrivals
#         ]
#         return arrival_data

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return []

# # Example usage
# if __name__ == "__main__":
#     # Replace these with your TfL API credentials
#     APP_ID = "your_app_id"
#     APP_KEY = "your_app_key"

#     # Replace with your desired bus stop code (naptanId or stopPointId)
#     BUS_STOP_CODE = "490008660N"

#     arrival_times = fetch_bus_arrival_times(BUS_STOP_CODE, APP_ID, APP_KEY)
#     if arrival_times:
#         print("Bus arrival times:")
#         for arrival in arrival_times:
#             print(f"Line: {arrival['lineName']} to {arrival['destinationName']} in {arrival['timeToStation']} minutes")
#     else:
#         print("No arrival information available.")

#this method will return us our actual coordinates
#using our ip address
import requests


def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
        #return lat, long
    except:
        #Displaying ther error message
        print('Internet Not avialable')
        #closing the program 
        exit()
        return False

print(locationCoordinates())