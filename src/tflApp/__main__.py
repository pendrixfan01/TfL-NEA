import requests
import folium
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


appID= os.getenv("appID")
appKey= os.getenv("appKey")


hammersmithDouble = ['HAMMERSMITH (DIST&PICC LINE)', 'HAMMERSMITH (H&C LINE)']
edgwareRoadDouble = ['EDGWARE ROAD (BAKERLOO)', 'EDGWARE ROAD (CIRCLE LINE)']
paddingtonDouble = ['PADDINGTON (DIST&BAKERLOO)', 'PADINGTON (H&C LINE)']


params = {
    "app_id": appID,
    "app_key": appKey,
}

def apiRequest(url):
        response = requests.get(url, params=params)
        print(response)
        return response

apiRequest('https://api.tfl.gov.uk/Line/piccadilly/Status')
def journeyPlanner(startLocation, endLocation):
    startLocation = getStationIDinFiles(startLocation, 'tube')
    endLocation = getStationIDinFiles(endLocation, 'tube')

    url = f"https://api.tfl.gov.uk/Journey/JourneyResults/{startLocation}/to/{endLocation}"
    


    response = apiRequest(url)

    if response.status_code == 200:
        journeyData = response.json()
        return journeyData
    else:
        print(f"Error: Unable to retrieve journey plan. Status code {response.status_code}")

def timeConvert(givenTime):
    timestamp = datetime.strptime(givenTime, '%Y-%m-%dT%H:%M:%S')
    human_readable = timestamp.strftime('%b %d, %Y, %I:%M %p')
    return human_readable

def displayJourneyPlan(journeyData):
    for journey in journeyData['journeys']:
        print("\n--- Journey Option ---")
        duration = journey['duration']
        print(f"Total journey time: {duration} minutes")
        
        for leg in journey['legs']:
            mode = leg['mode']['name']
            departurePoint = leg['departurePoint']['commonName']
            arrivalPoint = leg['arrivalPoint']['commonName']
            instruction = leg['instruction']['summary']

            departureTime = leg['departureTime']
            arrivalTime = leg['arrivalTime']
            departureTime = timeConvert(departureTime)
            arrivalTime = timeConvert(arrivalTime)

            print(f"\nMode: {mode}")
            print(f"From: {departurePoint}")
            print(f"To: {arrivalPoint}")
            print(f"Instruction: {instruction}")
            print(f"Departure time: {departureTime}")
            print(f"Arrival time: {arrivalTime}")
            

def getModeDisruptions(mode):
    url = f"https://api.tfl.gov.uk/Line/Mode/{mode}/Status"
    response = apiRequest(url)

    if response.status_code == 200:
        disruptions = response.json()
        return disruptions, mode
    else:
        print(f"Unable to retrieve response: status code {response.status_code}")


def reasonTrimmer(reason):
    charCount = 0
    for character in reason:
        if character != ':':
            reason = reason[:charCount] + reason[charCount+1:]
        else: 
            reason = reason.replace(':','')
            reason = reason.strip()
            return reason


def displayModeDisruptions(disruptions, mode):
    disCheck = False
    for line in disruptions:
        lineName = line.get("name")
        statuses = line.get("lineStatuses")

        for disruption in statuses:
            if disruption["statusSeverityDescription"] != "Good Service":
                disruptionReason = disruption.get("reason")
                disruptionReason = reasonTrimmer(disruptionReason)
                print(f"\n{lineName}: {disruption["statusSeverityDescription"]}\n{disruptionReason}\n")
                disCheck = True
            
            elif disCheck == False:
                pass


def getLineDisruptions(lineType):
        url = f"https://api.tfl.gov.uk/Line/{lineType}/Status"
        response = apiRequest(url)
        if response.status_code == 200:
            status = response.json()
            return status, lineType
        else:           
            print(f"Unable to retrieve response: status code {response.status_code}")

args = getLineDisruptions('victoria')
status = args[0]
lineType = args[1]
displayModeDisruptions(disruptions=status, mode=lineType)

def displayLineDisruptions(status, lineType):
    disruptionDescription = 81208
    for line in status:
        disruptions = line.get("lineStatuses")

        for disruption in disruptions:

                if disruptionDescription != disruption.get("reason"):
                    disruptionDescription = disruption.get("reason")
                    print(disruptionDescription)
                    if disruptionDescription is not None:
                        print(disruptionDescription)

                    else:
                        print(f'Good Service on the {lineType} Line.')

def getStationIDinFiles(stationName, mode):
    filePath = f'src/tflApp/resources/{mode}IDLookup.txt'
    with open(filePath, 'r') as lookupFile:
         for line in lookupFile:
                parts = line.strip()
                parts = parts.split(':')
                name, naptanID = parts

                if name.strip() == stationName.upper():
                    print(naptanID.strip())
                    return naptanID.strip()

def getStationArrivals(stationName, mode):
    stationID = getStationIDinFiles(stationName, mode)
    
    url = f"https://api.tfl.gov.uk/StopPoint/{stationID}/Arrivals"
    response = apiRequest(url)

    arrivalInfo = response.json()

    arrivalsByPlatform = {}

    for arrival in arrivalInfo:
        platformName = arrival['platformName']
        lineName = arrival['lineName']
        destination = arrival['destinationName']
        timeToPlatform = arrival['timeToStation'] / 60 #convert seconds to minutes
        timeToPlatform = round(timeToPlatform)

        if platformName not in arrivalsByPlatform:
            arrivalsByPlatform[platformName] = []

        if timeToPlatform < 30:
            arrivalsByPlatform[platformName].append({
                'line': lineName,
                'destination': destination,
                'timeToPlatform': timeToPlatform,
                })
    displayStationArrivals(arrivalsByPlatform)


def displayStationArrivals(arrivalsByplatform):
    for platform, predictions in arrivalsByplatform.items():
        if platform != "Platform Unknown":
            print(f'{platform}:')

            sorted_predictions = sorted(predictions, key=lambda x: x['timeToPlatform'])

            for prediction in sorted_predictions:
                lineName = prediction['line']
                destination = prediction['destination']
                arrivalTime = prediction['timeToPlatform']
                print(f'{lineName} Line to {destination} {arrivalTime}min\n')

#station = input().upper()
# match station:
#     case 'HAMMERSMITH':
#         for hammersmithStation in hammersmithDouble:
#             getStationArrivals(hammersmithStation, 'tube')
    
#     case 'EDGWARE ROAD':
#         for edgwareRoadStation in edgwareRoadDouble:
#             getStationArrivals(edgwareRoadStation, 'tube')

#     case 'PADDINGTON':
#         for paddingtonStation in paddingtonDouble:
#             getStationArrivals(paddingtonStation, 'tube')

#     case _:
#         mode = input()
#         getStationArrivals(station, mode)

