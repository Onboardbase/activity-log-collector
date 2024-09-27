
## Onboardbase Log Integration

This repo provides the necessary setup and code required to make onboardbase push logs to Wazuh Cluster.

Requirements:
- Wazuh Server
- Wazuh Agent
- Onboardbase Account(Follow [this](https://docs.onboardbase.com/reference/api-auth) to get an API Key)

### Installation
On a Wazuh Agent Server, run the below

Pre-Requisites

```bash
pip install requests
```

1. `git clone github.com/Onboardbase/onboardbase-wazuh`
2. `cd onboardbase-wazuh`
3.  Setup 
4. `bash ./setup.sh [ONBOARDBASE_API_KEY]`  # Sets up cron to pull data from onboardbase every 3 minutes

The setup collect logs at `/var/onboardbase/logs/remote_activity.log`

The logs for the last run can be viewed here: `/var/onboardbase/logs/cron.log`

Finally, setup your waz uh-agent or wazuh-server to collect logs from this file

```xml
<ossec_config>
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/onboardbase/logs/remote_activity.log</location>
  </localfile>
</ossec_config>
```

Confirm that the activity-log file is populated

```bash
tail -f /var/onboardbase/logs/remote_activity.log
```
