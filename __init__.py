from datetime import datetime

def timeConvert(givenTime):
    timestamp = datetime.strptime(givenTime, '%Y-%m-%dT%H:%M:%S')
    human_readable = timestamp.strftime('%b %d, %Y, %I:%M %p')
    print(human_readable)

timeConvert("2024-11-28T12:14:00")