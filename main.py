import os
import requests
import time


API_TOKEN = os.environ.get("DDNS_API_KEY")
if not API_TOKEN:
    raise RuntimeError("Missing environment variable DDNS_API_KEY")

BASE = "https://api.cloudflare.com/client/v4"
DOMAIN = "google.com"
FQDN = "mail.google.com"
SLEEP_TIME = 10 * 60


def cf_headers():
    return {
        "Authorization": f"Bearer {API_TOKEN}",  # Cloudflare uses Authorization: Bearer <token>
        "Content-Type": "application/json",
    }

def get_zone_id(zone_name: str) -> str:
    r = requests.get(
        f"{BASE}/zones",
        headers=cf_headers(),
        params={"name": zone_name, "status": "active"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("success") or not data.get("result"):
        raise RuntimeError(f"Failed to find zone_id for {zone_name}: {data}")
    return data["result"][0]["id"]

def get_record_id(zone_id: str, record_name: str, record_type: str) -> str:
    r = requests.get(
        f"{BASE}/zones/{zone_id}/dns_records",
        headers=cf_headers(),
        params={"name": record_name, "type": record_type, "per_page": 100},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("success") or not data.get("result"):
        raise RuntimeError(f"Failed to find record_id for {record_type} {record_name}: {data}")
    return data["result"][0]["id"]

def overwrite_dns_record(
    zone_id: str,
    record_id: str,
    record_type: str,
    record_name: str,
    content: str,
    ttl: int = 1,          # 1 means "auto" for many record types
    proxied: bool = False  # only relevant for some record types (A/AAAA/CNAME)
) -> dict:
    payload = {
        "type": record_type,
        "name": record_name,
        "content": content,
        "ttl": ttl,
        "proxied": proxied,
    }

    r = requests.put(
        f"{BASE}/zones/{zone_id}/dns_records/{record_id}",
        headers=cf_headers(),
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(f"Cloudflare API error: {data}")
    return data["result"]


def updateDns(newIp: str):
    zone_id = get_zone_id(DOMAIN)
    record_id = get_record_id(zone_id, FQDN, "A")

    result = overwrite_dns_record(
        zone_id=zone_id,
        record_id=record_id,
        record_type="A",
        record_name=FQDN,
        content=newIp,
        ttl=1,
        proxied=False,
    )
    print("Updated:", result["id"], result["name"], "->", result["content"])



def main():

    oldIp = None

    while True:
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        
        if ip != oldIp:
            updateDns(ip)
            oldIp = ip
            print(f"Updated DNS to: {ip}")

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()

