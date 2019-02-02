# Meetup Group Admin Tool

This project's purpose is to overcome the limitations of the new Meetup UI for group administrators to take attendance and reconcile payments external to the meetup platform.

## Dependencies

* Python3

## Usage
```
python3 -m meetup.AttendeeListGenerator MEETUP_API_KEY MEETUP_GROUP > attendance.html
```
* `MEETUP_API_KEY`  - Obtained from [Meetup API Website](https://secure.meetup.com/meetup_api/key/)
* `MEETUP_GROUP` - The group name as found in the URL, e.g. Sydney-Hotshots