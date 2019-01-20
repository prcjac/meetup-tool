import sys

def attendeeListGenerator(apiKey, group):
    pass

def printUsage():
    print("python3 " + sys.argv[0] + " MEETUP_API_KEY MEETUP_GROUP_NAME")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)
    else:
        sys.exit(attendeeListGenerator)