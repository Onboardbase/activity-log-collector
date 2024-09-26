import requests
from datetime import datetime
from os import getenv
import socket
import os

# API URL
url = "https://public.onboardbase.com/api/v1/activity-logs"

# Path to the file where the last timestamp is saved
timestamp_file = "/etc/onboardbase/logs/last_run_timestamp"
output_file = "/var/onboardbase/logs/remote_activity.log"

# Get system hostname for the syslog format
hostname = socket.gethostname()

# Define APP-NAME and PROCID for the syslog format
app_name = "onboardbase_activity_logs"
procid = os.getpid()


def get_last_run_time():
    """Reads the last run timestamp from file or returns None if the file doesn't exist."""
    try:
        with open(timestamp_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_last_run_time(timestamp):
    """Writes the current timestamp to the file."""
    with open(timestamp_file, "w") as f:
        f.write(timestamp)


def format_log(log):
    """Formats the log data for better readability."""
    user_info = log.get("user", {})
    team_info = log.get("team", {})
    project_info = log.get("project", {})
    secret_env_info = log.get("secretEnvironment", {})

    return {
        "IP Address": log.get("ip"),
        "City": log.get("city"),
        "Country": log.get("country"),
        "Date Added": log.get("dateAdded"),
        "Activity Type": log.get("type"),
        "Platform": log.get("platform"),
        "User Name": user_info.get("name"),
        "User Email": user_info.get("email"),
        "Team Name": team_info.get("name"),
        "Project Title": project_info.get("title"),
        "Secret Environment": secret_env_info.get("title"),
        "Count": log.get("count", 0)  # Include count in formatted log
    }


def generate_syslog_message(priority, log):
    """Generates a syslog message using standard format."""

    original_timestamp = log.get("Date Added")
    if original_timestamp:
        timestamp = datetime.fromisoformat(original_timestamp[:-1]).strftime("%b %d %H:%M:%S")
    else:
        timestamp = datetime.now().strftime("%b %d %H:%M:%S") 

    activity_type = log.get("Activity Type", "UNKNOWN")

    activity_type = log.get("Activity Type", "UNKNOWN")
    count = log.get("Count", 0)

    message = (f"User {log.get('User Name')} from team {log.get('Team Name')} "
               f"performed {activity_type} on project {log.get('Project Title')} "
               f"in environment {log.get('Secret Environment')} (Count: {count}).")

    syslog_msg = f"<{priority}> {timestamp} {hostname} {app_name}[{procid}]: {activity_type} {message}"
    return syslog_msg


def fetch_logs(after_time):
    """Fetch logs from API using the last timestamp as the 'after' parameter."""
    params = {
        "project": getenv("ONBOARDBASE_PROJECT"),
        "skip": 0,
        "take": 10,
        "after": after_time
    }

    headers = {
        "API_KEY": getenv("ONBOARDBASE_PUBLIC_API_KEY")
    }

    try:
        # Send GET request to the API
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # Parse JSON response
        result = response.json()

        if result.get("status") == "success" and result.get("totalCount", 0) > 0:
            logs = result.get("data", [])

            # Append logs to the output file in syslog format
            with open(output_file, "a") as f:
                for log in logs:
                    formatted_log = format_log(log)

                    # Set the priority (facility = 1 (user-level), severity = 6 (informational))
                    priority = 14  # PRI = (1 * 8) + 6
                    syslog_message = generate_syslog_message(priority, formatted_log)

                    # Write the syslog message to the file
                    f.write(syslog_message + "\n")

            print(f"Logs appended in syslog format")
        else:
            print("No new logs to append.")

        # Save the current time as the new 'after' time
        save_last_run_time(datetime.now().isoformat())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


# Get the last run time or use a default start time
last_run_time = get_last_run_time()
if last_run_time is None:
    # If no previous timestamp, use a default (e.g., 2023-11-12T13:26:32.684Z)
    last_run_time = "2023-11-12T13:26:32.684Z"

# Fetch logs and update the last run timestamp
fetch_logs(last_run_time)
