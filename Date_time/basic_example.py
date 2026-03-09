from datetime import date, time, datetime, timedelta


# Function to display information about a date
def show_date_info(given_date: date) -> None:
    print("Date:", given_date)

    # Access individual components of the date
    print("Day:", given_date.day)
    print("Month:", given_date.month)
    print("Year:", given_date.year)

    # weekday() returns the day of the week
    # Monday = 0, Sunday = 6
    print("Weekday (0=Monday):", given_date.weekday())

    # ISO format is a standard date representation (YYYY-MM-DD)
    print("ISO format:", given_date.isoformat())
    print()


# Function to display information about a time object
def show_time_info(given_time: time) -> None:
    # Print the full time
    print("Time:", given_time)

    # Access hour, minute, and second components
    print("Hour:", given_time.hour)
    print("Minute:", given_time.minute)
    print("Second:", given_time.second)
    print()


# Function to display information about current datetime
def show_datetime_info(current_datetime: datetime) -> None:
    # Print the current date and time
    print("Current datetime:", current_datetime)

    # Extract only the date part
    print("Date part:", current_datetime.date())

    # Extract only the time part
    print("Time part:", current_datetime.time())
    print()


# Function demonstrating timedelta operations
def show_timedelta_examples() -> None:
    # Create a time difference of 5 days, 3 hours, and 30 minutes
    delta = timedelta(days=5, hours=3, minutes=30)

    # Get the current date and time
    now = datetime.now()

    print("Timedelta:", delta)
    print("Current datetime:", now)

    # Add the timedelta to the current datetime
    print("After adding timedelta:", now + delta)

    # Subtract the timedelta from the current datetime
    print("After subtracting timedelta:", now - delta)
    print()


# Main function to organize program execution
def main() -> None:
    # Create a sample date object
    sample_date = date(2026, 11, 23)

    # Create a sample time object
    sample_time = time(20, 45, 31)

    # Get the current datetime from the system
    current_datetime = datetime.now()

    # Call the functions to display information
    show_date_info(sample_date)
    show_time_info(sample_time)
    show_datetime_info(current_datetime)
    show_timedelta_examples()


# This ensures the main() function runs only when the script is executed directly
if __name__ == "__main__":
    main()