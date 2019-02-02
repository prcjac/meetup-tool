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
    return 0

def renderEventDetails(event, rsvps):
    title = event["name"] + " - " + event["local_time"] + " " + event["local_date"]
    print("<html><head><title>%s</title><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css\"></head>" % title)
    print("<body>")
    print("<h1>%s</h1>" % title)
    print("<h2>%s</h2>" % event["group"]["name"])
    print("<table class=\"table table-striped\">")
    print("<thead class=\"thead-dark\"><tr><th colspan=\"2\">Member</th><th>Guests</th><th>Status</th><th>Attended</th><th>Paid</th><th>Reconciled</th></tr></thead>")
    print("<tbody>")
    attendees = [rsvp for rsvp in rsvps if rsvp["response"] == "yes"]
    waitlists = [rsvp for rsvp in rsvps if rsvp["response"] == "waitlist"]

    for rsvp in attendees:
        renderRow(rsvp, "Attending")

    for rsvp in waitlists:
        renderRow(rsvp, "Waitlist")

    for i in range(0,5):
        print("<tr><td>Additional %d:</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" % (i + 1))

    attendeeCount = countRsvps(attendees)
    waitlistCount = countRsvps(waitlists)

    print("<tr><td><b>Total</b></td><td>Attending: %d, Waitlist: %d</td><td></td><td></td><td></td><td></td><td></td></tr>" % (attendeeCount, waitlistCount))
    print("</tbody></table>")
    print("<body>")
    print("</html>")

def renderRow(rsvp, status):
    print("<tr><td>%s</td><td>%s</td><td>%d</td><td>%s</td><td></td><td></td><td></td></tr>" % (
        "<img src=\"%s\"/>" % rsvp["member"]["photo"]["thumb_link"] if "photo" in rsvp["member"] else "",
        rsvp["member"]["name"],
        rsvp["guests"],
        status))

def countRsvps(rsvps):
    count = 0
    for rsvp in rsvps:
        count += 1
        count += int(rsvp["guests"])
    return count

def printUsage():
    print("python3 " + sys.argv[0] + " MEETUP_API_KEY MEETUP_GROUP_NAME")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)
    else:
        sys.exit(attendeeListGenerator(sys.argv[1], sys.argv[2]))