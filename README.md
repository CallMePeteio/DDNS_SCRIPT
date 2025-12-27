


----------------- SET API KEY:

Log in to Cloudflare
Click your profile avatar (top-right)
Go to My Profile
Select API Tokens
Click Create Token
Choose Create Custom Token

Permissions:      Zone → DNS → Edit
Zone Resources:   Include → Specific zone → example.com

- On machine that runs script (change string) linux
export DDNS_API_KEY="COPIED_KEY"



----------------- UPDATE VARIABLES INSIDE MAIN.PY:
DOMAIN = "google.com"
FQDN = "mail.google.com"
SLEEP_TIME = 10 * 60     -Seconds, how long untill next check


----------------- RUN PYTHON SCRIPT:
python3 main.py




