

Cloudflare DDNS Python Script

This project provides a simple Python-based Dynamic DNS (DDNS) updater using the Cloudflare API. It periodically checks your public IP address and updates a DNS record when changes are detected.

Prerequisites

Python 3.x

A Cloudflare account

A domain managed by Cloudflare

Linux-based system (or compatible shell environment)

1. Create a Cloudflare API Token

Log in to Cloudflare.

Click your profile avatar (top-right).

Go to My Profile.

Select API Tokens.

Click Create Token.

Choose Create Custom Token.

Token Configuration

Permissions

Zone → DNS → Edit

Zone Resources

Include → Specific zone → example.com

After creating the token, copy it for later use.

2. Set the API Key Environment Variable

On the machine that will run the script (Linux):

export DDNS_API_KEY="YOUR_CLOUDFLARE_API_TOKEN"


To make this persistent, add the line above to your shell profile (e.g. .bashrc or .profile).

3. Configure main.py

Edit the following variables in main.py:

DOMAIN = "google.com"
FQDN = "mail.google.com"
SLEEP_TIME = 10 * 60  # Seconds between checks

Variable Description

DOMAIN
The Cloudflare-managed zone (root domain).

FQDN
The fully qualified domain name (DNS record) to update.

SLEEP_TIME
Interval, in seconds, between IP checks.

4. Run the Script

Execute the script using Python:

python3 main.py


The script will continue running and periodically update the DNS record if your public IP address changes.

Notes

Ensure the API token has only the permissions listed above.

The script is intended to run continuously (e.g. via tmux, screen, or a system service).

Logging/output behavior depends on the implementation in main.py.




