# Meetup Group Admin Tool

This project's purpose is to overcome the limitations of the new Meetup UI for group administrators to take attendence and reconsile payments external to the meetup platform.

## Dependencies

* Python3

## Usage
```
python3 -m meetup.AttendeeListGenerator MEETUP_API_KEY MEETUP_GROUP > attendance.html
```
* `MEETUP_API_KEY`  - Obtained from [https://secure.meetup.com/meetup_api/key/](Meetup API website)
* `MEETUP_GROUP` - The group name as found in the URL, e.g. Sydney-Hotshots