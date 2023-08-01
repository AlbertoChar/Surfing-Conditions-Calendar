# Surfing-Conditions-Calendar
The Surfing Conditions Calendar is a Python project that utilizes real-time ocean data to create a convenient calendar of upcoming surfing conditions. 

**Introduction**

This Python project fetches real-time ocean conditions, including wave height, direction, and period, using the Open Meteo API. It then creates a convenient calendar with surfing events for the upcoming week. The generated iCalendar (ICS) file can be easily imported into your favorite calendar app, allowing you to stay updated on the best surfing conditions in your area!


Clone this repository to your local machine.
Navigate to the project directory.
Install the required libraries mentioned in the Prerequisites section.
Run the surfing_conditions.py script using Python: python surfing_conditions.py
The script will fetch the surfing conditions for the next week, filter the data, and display it in a table.
An iCalendar file named surfing_events.ics will be generated in the project directory, containing the surfing events for the upcoming week.
Configuration

In the get_surfing_conditions function, update the latitude and longitude values in the API URL to match your desired surfing location.
