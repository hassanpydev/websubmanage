import CloudFlare


def create_subdomain_dns_record(subdomain,zone_name=None):
    cf = CloudFlare.CloudFlare(
        certtoken="v1.0-4ecb6fa2b427c0ec2b66a91c-9b92e59583349702eeb76ee5fee4eab750537c49d011842605e6bb166fc4c14df36781936a3fe92c55e433ccce5ae9085369907a09873fb9e0d60d2a37039e0ab8d4b889bb08a79b35",
        email="akraaonline@gmail.com",
        token="e535e60c2fd491a5b17c1fffac1faecf274da",
    )
    zones = cf.zones.get()
    zone_name = "websubmange.com"

    zone_id = None
    for zone in zones:
        if zone["name"] == zone_name:
            zone_id = zone["id"]
            break

    if not zone_id:
        print(f"Zone ID not found for Zone Name: {zone_name}")
        exit()

    # Specify the DNS record details
    record_type = "A"  # Example: A, CNAME, MX, etc.
    record_name = subdomain  # Example: subdomain.example.com
    record_content = "89.117.50.15"  # Example: IP address or domain name
    record_ttl = 3600  # Example: Time-to-Live value in seconds

    # Construct the DNS record data
    dns_record = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": record_ttl,
        "proxied": True
    }

    # Add DNS record to CloudFlare
    result = cf.zones.dns_records.post(zone_id, data=dns_record)
    print(result)
    # Check if DNS record was added successfully
