import json

files = ['bom', 'rds', 'rtl', 'rai', 'la7', 'mediaset', 'radiokisskiss', 'radioliberta', 'nove', 'realtime', 'sportitalia', 'twentyseven_mediaset']

domains_before_consent = []

#EXAMPLE: {"example.com": {"ips": [192.168.1.1], "consent_status": ["consent_revoked"]}}

for file in files:

    updated_map = {}

    dns_map = json.load(open('../dns_mapping/' + file + '.json', 'r'))
    consent_status = json.load(open('../consent_status/' + file + '.json', 'r'))

    for ip, consent in consent_status.items():
        try:
            domain = dns_map[ip]
            try:
                updated_map[domain]['ip'].append(ip)
                for element in consent:
                    if element not in updated_map[domain]['consent_status']:
                        updated_map[domain]['consent_status'].append(element)
            except:
                updated_map[domain] = {}
                updated_map[domain]['ip'] = [ip]
                updated_map[domain]['consent_status'] = consent
        except:
            try:
                updated_map[ip]['ip'].append(ip)
                for element in consent:
                    if element not in updated_map[ip]['consent_status']:
                        updated_map[ip]['consent_status'].append(element)
            except:
                updated_map[ip] = {}
                updated_map[ip]['ip'] = [ip]
                updated_map[ip]['consent_status'] = consent
    
    json.dump(updated_map, open('../full_analysis/' + file + '.json', 'w+'))

    for key, value in updated_map.items():
        if 'before_consent' in value['consent_status']:
            domains_before_consent.append(key)

    print("Domains before consent for ", file, ":", domains_before_consent)                