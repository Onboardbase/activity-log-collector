#!/bin/bash

if [[ -z $1 ]]; then
  echo "The first argument must be an API KEY from your onboardbase dashboard"
  exit 1
fi

if [[ -z $2 ]]; then
  echo "The second argument (name of project) is not supplied. This would get logs for all projects"
fi

# Path to your Python script
SCRIPT_NAME="$(dirname "${BASH_SOURCE[0]}")/fetch_onboardbase_logs.py"
SCRIPT_PATH=$(readlink -f $SCRIPT_NAME)

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: The script at $SCRIPT_PATH does not exist."
    exit 1
fi

mkdir -p "/var/onboardbase/logs"
mkdir -p "/etc/onboardbase/logs"



 # Create a temporary file to hold the current crontab
 TEMP_CRONTAB=$(mktemp)

 # Get the current crontab
 crontab -l > "$TEMP_CRONTAB"

 # Add the new cron job (every 3 minutes)
 # Adjust the command to activate your Python environment if necessary
 echo "*/3 * * * * ONBOARDBASE_PUBLIC_API_KEY=${1} ONBOARDBASE_PROJECT=${2} /usr/bin/python3 $SCRIPT_PATH >> /var/onboardbase/logs/cron.log 2>&1" >> "$TEMP_CRONTAB"

 # Install the new crontab
 crontab "$TEMP_CRONTAB"

 # Remove the temporary file
 rm "$TEMP_CRONTAB"

 echo "Cron job added: Run $SCRIPT_PATH every 3 minutes."