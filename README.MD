
## Onboardbase Log Integration

This repo provides the necessary setup and code required to make onboardbase push logs to Wazuh Cluster.

Requirements:
- Wazuh server
- Wazuh agent
- Onboardbase account(Follow [this](https://docs.onboardbase.com/reference/api-auth) to get an API Key)

### Installation
On a Wazuh agent server, run the below

Pre-Requisites

---
```bash
pip install requests
```
---

1. `git clone https://github.com/Onboardbase/activity-log-collector.git onboardbase-activity-log-collector`
2. `cd onboardbase-activity-log-collector`
3.  Sets up cron to pull data from onboardbase every 3 minutes
4. `bash ./setup.sh [ONBOARDBASE_API_KEY] [ONBOARDBASE_PROJECT_NAME]`

The setup collect logs at `/var/onboardbase/logs/remote_activity.log`.

The logs for the last run can be viewed here: `/var/onboardbase/logs/cron.log`.

Finally, setup your wazuh-agent or wazuh-server to collect logs from this file.

[Wazuh Documentation - Monitoring Basic Logfiles](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/monitoring-log-files.html#monitoring-basic-log-files)

---
```xml
<ossec_config>
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/onboardbase/logs/remote_activity.log</location>
  </localfile>
</ossec_config>
```
---

Confirm that the activity-log file is populated.

---
```bash
tail -f /var/onboardbase/logs/remote_activity.log
```
---

### Staying updated
Please maintain this repo anywhere it is been setup. Bug and improvements would be pushed directly to the upstream.

You only need to come to the directory where this repo is and run:

```bash
git pull
```

Since the script runs via a cron job, the changes would be picked automatically on the next run.
