from http.client import HTTPSConnection
import json
import sys

def attendeeListGenerator(apiKey, group):
    httpsConnection = HTTPSConnection("api.meetup.com")
    headers = {
        "Content-Type": "application/json"
    }

    httpsConnection.request("GET", "/%s/events?key=%s&status=upcoming" % (group, apiKey), headers = headers)

    try:
        response = httpsConnection.getresponse()
        responseString = response.read().decode("utf-8")
        responseCode = response.getcode()
        if responseCode == 200:
            events = json.loads(responseString)
        else:
            print(str(responseCode) + " returned")
            return 1
    except ConnectionError as e:
        print("Unable to connect to Meetup API")
        print(e)
        return 1
    except json.JSONDecodeError:
        print("Invalid JSON returned")
        return 1

    if len(events):
        event = events[0]
        eventId = event["id"]
        httpsConnection.request("GET", "/%s/events/%s/rsvps?key=%s" % (group, eventId, apiKey), headers=headers)
        try:
            response = httpsConnection.getresponse()
            responseString = response.read().decode("utf-8")
            responseCode = response.getcode()
            if responseCode == 200:
                rsvps = json.loads(responseString)
            else:
                print(str(responseCode) + " returned")
                return 1
        except ConnectionError as e:
            print("Unable to connect to Meetup API")
            print(e)
            return 1
        except json.JSONDecodeError:
            print("Invalid JSON returned")
            return 1
    else:
        print("No events returned")
        return 1

    renderEventDetails(event, rsvps)

def renderEventDetails(event, rsvps):
    print(event["group"]["name"])
    print(event["name"])
    print(event["local_time"] + " " + event["local_date"])
    print()
    for rsvp in  rsvps:
        print(rsvp["member"]["name"] + " " + str(rsvp["guests"]) + (rsvp["member"]["photo"]["photo_link"] if "photo" in rsvp["member"] else " "))
    pass

def printUsage():
    print("python3 " + sys.argv[0] + " MEETUP_API_KEY MEETUP_GROUP_NAME")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)
    else:
        sys.exit(attendeeListGenerator(sys.argv[1], sys.argv[2]))