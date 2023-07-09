import json

occurrences_domains = {}

files = ['rai', 'rds', 'rtl', 'bom', 'la7', 'mediaset', 'radiokisskiss', 'radioliberta', 'nove', 'realtime', 'sportitalia', 'twentyseven_mediaset']

for file in files:
    mapping = json.load(open('../full_analysis/' + file + '.json', 'r'))

    for domain,value in mapping.items():

        try:
            occurrences_domains[domain] += 1
        except:
            occurrences_domains[domain] = 1

excluded_ips = []

for key,value in occurrences_domains.items():
    if value > 4:
        excluded_ips.append(key)

print(excluded_ips)