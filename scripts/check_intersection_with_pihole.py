import re, os, json

base_path = 'blocklists/pihole/'

files = ['rai', 'rds', 'rtl', 'bom', 'la7', 'mediaset', 'radiokisskiss', 'radioliberta', 'nove', 'realtime', 'sportitalia', 'twentyseven_mediaset']

for file in files:
    domains = json.load(open('../full_analysis/domains_before_consent/' + file + '.json'))
    blocked_domains = set()

    for blocklist in os.listdir(base_path):

        blocklist_items = open(base_path + blocklist, 'r').readlines()

        for domain in domains:
            for item in blocklist_items:
                if re.search(domain, item) != None:
                    blocked_domains.add(domain)

    print("Analyzing", file)
    print(blocked_domains)
    print(len(blocked_domains), '\n')