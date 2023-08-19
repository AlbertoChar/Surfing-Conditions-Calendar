from datetime import timedelta

import arrow
import requests
from tabulate import tabulate
from flask import Flask, jsonify


def get_surfing_conditions():
    # Get the start and end dates for the next week
    start_date = arrow.now().floor('day')  # Start from the next day
    end_date = start_date.shift(days=6)

    url = f'https://marine-api.open-meteo.com/v1/marine?latitude=32.0809&longitude=34.7806&hourly=wave_height,wave_direction,wave_period&start_date={start_date.format("YYYY-MM-DD")}&end_date={end_date.format("YYYY-MM-DD")}'

    response = requests.get(url)
    jsonData = response.json()

    # Extract the hourly data for each parameter
    hourly_data = jsonData['hourly']

    # Create a list of dictionaries to store the filtered data in a tabular format
    filtered_data = []
    for i in range(len(hourly_data['time'])):
        time = arrow.get(hourly_data['time'][i])

        # Filter hours between 10 am to 7 pm and include only every two hours
        if 10 <= time.hour < 19 and time.hour % 2 == 0:
            wave_height = hourly_data['wave_height'][i]
            wave_direction = hourly_data['wave_direction'][i]
            wave_period = hourly_data['wave_period'][i]
            filtered_data.append({'Time (GMT+3)': time.format('YYYY-MM-DD HH:mm'), 'Wave Height (m)': wave_height,
                                  'Wave Direction (°)': wave_direction, 'Wave Period (s)': wave_period})

    return filtered_data


def display_table(data):
    # Display the filtered data in a table
    table_str = tabulate(data, headers='keys', tablefmt='grid')
    print(table_str)
    return table_str


def generate_ics_event(item):
    time = arrow.get(item['Time (GMT+3)'], 'YYYY-MM-DD HH:mm')
    start_time = time.to('utc').format('YYYYMMDDTHHmmss') + 'Z'
    end_time = (time + timedelta(minutes=10)).to('utc').format('YYYYMMDDTHHmmss') + 'Z'

    wave_height = item['Wave Height (m)']
    wave_direction = item['Wave Direction (°)']
    wave_period = item['Wave Period (s)']

    summary = f"Wave height: {wave_height}m"
    description = f"Wave Height: {wave_height} m, Wave Direction: {wave_direction}°, Wave Period: {wave_period} s"
    location = 'Tel Aviv, Israel'

    ics_event = f"BEGIN:VEVENT\nDTSTART;TZID=Asia/Jerusalem:{start_time}\nDTEND;TZID=Asia/Jerusalem:{end_time}\nSUMMARY:{summary}\nDESCRIPTION:{description}\nLOCATION:{location}\nEND:VEVENT"

    return ics_event


def generate_ics_data(filtered_data):
    ics_data = []
    for item in filtered_data:
        ics_event = generate_ics_event(item)
        ics_data.append(ics_event)

    return '\n'.join(ics_data)


def write_ics_file(ics_data, file_path):
    with open(file_path, 'w') as file:
        file.write(f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:\n{ics_data}\nEND:VCALENDAR")


def main():
    surfing_conditions = get_surfing_conditions()
    table_str = display_table(surfing_conditions)

    # Create iCalendar events
    ics_data = generate_ics_data(surfing_conditions)
    write_ics_file(ics_data, 'surfing_events.ics')


if __name__ == "__main__":
    main()
