from adblockparser import AdblockRules
import lzma, os
import json

base_path = 'blocklists/'
base_path_old_lists = 'easylist/'

easylist = [x.strip() for x in open(base_path + 'easylist/easylist_annoyance_27_05_2022.txt', 'r').readlines()]
rules = AdblockRules(easylist)

files = ['rai', 'rds', 'rtl', 'bom', 'la7', 'mediaset', 'radiokisskiss', 'radioliberta', 'nove', 'realtime', 'sportitalia', 'twentyseven_mediaset']

'''for file in files:

    domains = json.load(open('full_analysis/domains_before_consent/' + file + '.json'))
    blocked_domains = set()

    for domain in domains:
        updated_domain = 'http://' + domain
        if rules.should_block(updated_domain):
            blocked_domains.add(domain)
        if rules.should_block(domain):
            blocked_domains.add(domain)

    print("Analyzing", file)
    print(blocked_domains)
    print(len(blocked_domains), '\n')'''


for file in files:
    domains = json.load(open('full_analysis/domains_before_consent/' + file + '.json'))
    blocked_domains = set()

    for list in os.listdir(base_path_old_lists):
        easylist_file = os.path.join(base_path_old_lists, list)
        easylist = [x.strip() for x in lzma.open(easylist_file, mode='rt', encoding='utf-8').readlines()]

        rules = AdblockRules(easylist)

        for domain in domains:
            updated_domain = 'http://' + domain
            if rules.should_block(updated_domain):
                blocked_domains.add(domain)
            if rules.should_block(domain):
                blocked_domains.add(domain)

    print("Analyzing", file)
    print(blocked_domains)
    print(len(blocked_domains), '\n')
