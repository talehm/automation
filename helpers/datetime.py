from datetime import datetime, timedelta

# Define the fixed hours for each day of the week
day_hours = {
    "Monday": ["02:00-05:00"],
    "Tuesday": ["02:00-05:00"],
    "Wednesday": ["02:00-05:00", "20:00-22:00"],
    "Thursday": ["02:00-05:00", "20:00-22:00"],
    "Friday": ["02:00-05:00", "20:00-22:00"],
    "Saturday": ["02:00-05:00", "20:00-22:00"],
    "Sunday": ["02:00-05:00"],
}


# Convert "HH:MM-HH:MM" format to timedelta (minutes)
def parse_hours(time_range):
    start_time, end_time = time_range.split("-")
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))

    # Convert times to timedelta from midnight for easy calculation
    start_dt = timedelta(hours=start_hour, minutes=start_minute)
    end_dt = timedelta(hours=end_hour, minutes=end_minute)

    return start_dt, end_dt


def generate_datetime_strings(count, days=0):
    """
    Generate sorted datetime strings based on fixed time ranges,
    starting from the next day's valid range at 02:00.

    Args:
    - count (int): Number of datetime strings to generate.

    Returns:
    - list of str: List of sorted datetime strings in "YYYY-MM-DDTHH:MM" format.
    """
    # Get the current date and time
    now = datetime.now() + timedelta(days=days)
    now = datetime(now.year, now.month, now.day)
    print(now)
    # Move to the next day's 00:00 (midnight)
    next_day = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
        days=1
    )

    # List to store the generated datetime strings
    datetime_strings = []

    # The required count of datetime strings per day
    daily_count = 100

    # Loop to generate datetimes until count is reached
    valid_count = 0
    while valid_count < count:
        # Get the current day's name
        day_name = next_day.strftime("%A")

        # Get the time ranges for the current day
        time_ranges = day_hours.get(day_name, [])

        # Debug: print the current date and day
        print(f"Processing date: {next_day.strftime('%Y-%m-%d')} ({day_name})")

        # Check if the day has valid ranges
        if not time_ranges:
            # If no valid ranges, skip to the next day
            next_day += timedelta(days=1)
            continue

        # Check today's time range first (if it's today)
        if now.date() == next_day.date():
            # Loop over all time ranges for today
            for time_range in time_ranges:
                start_dt, end_dt = parse_hours(time_range)

                # Convert to datetime objects for today's date
                start_time = next_day + start_dt
                end_time = next_day + end_dt

                # Ensure we're processing the next available time
                if start_time >= now:  # Don't skip if it's today and valid time
                    # Generate datetime strings for this time range
                    current_time = start_time
                    daily_generated = 0
                    while current_time <= end_time and daily_generated < daily_count:
                        # Add the valid datetime string to the list
                        datetime_strings.append(current_time.strftime("%Y-%m-%dT%H:%M"))
                        daily_generated += 1
                        valid_count += 1

                        # Stop when we've reached the total required count
                        if valid_count >= count:
                            break

                        # Move to the next datetime string
                        interval = (end_time - start_time).total_seconds() / (
                            daily_count - daily_generated
                        )
                        current_time += timedelta(seconds=interval)

                    # Stop processing ranges if we've met the required count
                    if valid_count >= count:
                        break
            # If today is done and we have enough valid datetimes, move to the next day
            if valid_count >= count:
                break
        else:
            # If it's not today, process the next day's ranges normally
            for time_range in time_ranges:
                start_dt, end_dt = parse_hours(time_range)

                # Convert to datetime objects for the next day
                start_time = next_day + start_dt
                end_time = next_day + end_dt

                # Generate datetime strings for this time range
                current_time = start_time
                daily_generated = 0
                while current_time <= end_time and daily_generated < daily_count:
                    # Add the valid datetime string to the list
                    datetime_strings.append(current_time.strftime("%Y-%m-%dT%H:%M"))
                    daily_generated += 1
                    valid_count += 1

                    # Stop when we've reached the total required count
                    if valid_count >= count:
                        break

                    # Move to the next datetime string
                    interval = (end_time - start_time).total_seconds() / (
                        daily_count - daily_generated
                    )
                    current_time += timedelta(seconds=interval)

            # Move to the next day after processing all ranges
            next_day += timedelta(days=1)

    # Return sorted datetime strings
    return datetime_strings
