
## Onboardbase Log Integration

This repo provides the neccasary setup and code required to make onboardbase push logs to Wazuh Cluster.

Requirements:
- Wazuh Server
- Wazuh Agent
- Onboardbase Account(Follow this to get an API Key)

### Installation
On a Wazuh Agent Server, run the below

1. `git clone github.com/Onboardbase/onboardbase-wazuh`
2. `cd onboardbase-wazuh`
3.  Setup 
4. `bash -c ./setup.sh`  # Sets up cron to pull data from onboardbase every 3 minutes

The setup ensures collect logs at `~/.onboardbase/logs/remote_activity_logs`

---
```go
```bash
pip install requests
```
```
---
