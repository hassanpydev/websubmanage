import CloudFlare


def create_subdomain_dns_record(subdomain):
    cf = CloudFlare.CloudFlare(
        certtoken="v1.0-9298b9cc78d451e6193d8346-804d523e23dd9bb951374eec14876820d25551b9b274776ce1516dea8831b60d8d55c2421b246a29d623ee81db976cde8e985942214460d72f31c4668e3665677bc299ef871bd37d52",
        email="halsmiri@ucas.edu.ps",
        token="c6b1966ee462a6621061cce11c0756ba86326",
    )
    zones = cf.zones.get()
    zone_name = "demosite.com"

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
    record_content = "1.1.1.1"  # Example: IP address or domain name
    record_ttl = 3600  # Example: Time-to-Live value in seconds

    # Construct the DNS record data
    dns_record = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": record_ttl,
    }

    # Add DNS record to CloudFlare
    result = cf.zones.dns_records.post(zone_id, data=dns_record)
    print(result)
    # Check if DNS record was added successfully
