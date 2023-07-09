import pyshark, signal, os
from adblockparser import AdblockRules
import re, json, hashlib, requests
from threading import Thread, Event
from time import sleep
from datetime import date, datetime

CHANNEL_PATTERNS = [('mediaset', 'Mediaset'), ('rai', 'Rai'), ('kbbtv', 'ParamountNetwork'), ('sportitalia', 'Sportitalia'), 
    ('smartclip', 'Sportitalia'), ('rds', 'RDS'), ('castoola', 'Discovery'), ('dplayservices', 'Discovery'),
    ('rtl', 'RTL'), ('kisscms', 'RadioKissKiss'), ('timvision', 'Cairo'), ('limone', 'Cairo')]

EASYLIST = [x.strip() for x in open('easylist.txt', 'r').readlines()]
PIHOLE = [x.strip() for x in open('pihole.txt', 'r').readlines()]

TRACKING_DOMAIN = set()

IPTABLE_RULES = []

NETWORK_INTERFACE = json.load(open('hash_and_dates.json', 'r'))['network_interface']
CURRENT_HASH = json.load(open('hash_and_dates.json', 'r'))['config_hash']

OLD_CONF = json.load(open('config.json', 'r'))

PREVIOUS_CHANNEL = None
CHANNEL_INFO = None

def check_channel(d):

    for pattern in CHANNEL_PATTERNS:
        if pattern[0] in d:
            return pattern[1]

    return None

def check_domain_in_pihole(d):
    for pattern in PIHOLE:
        if re.search(d, pattern) != None:
            TRACKING_DOMAIN.add(d)

def check_domain_in_easylist(d):
    rules = AdblockRules(EASYLIST)
    if rules.should_block(d):
        TRACKING_DOMAIN.add(d)

# https://stackoverflow.com/questions/2957116/how-to-run-multiple-functions-at-the-same-time
def check_incoming_packets():

    #listen continuosly to traffic
    for packet in capture.sniff_continuously():
        try:
            if packet.udp.port == '53' and packet.dns.qry_type == '1':
                #check the contacted domain in the DNS request
                contacted_domain = packet.dns.resp_name

                print("Contacted host:", contacted_domain)

                
                # Check which Channel is being watched
                CHANNEL_INFO = check_channel(contacted_domain)

                if contacted_domain not in TRACKING_DOMAIN:
                    check_domain_in_pihole(contacted_domain)
                    check_domain_in_easylist(contacted_domain)

                    if len(TRACKING_DOMAIN) != 0:
                        json.dump(list(TRACKING_DOMAIN), open('tracking_domains_lists.json', 'w+'))

            if exit_event.is_set():
                break

        except:
            pass

def check_http(http_value):
    if http_value == "allow":
        os.system("iptables -D FORWARD -i " + NETWORK_INTERFACE + " -p tcp --destination-port 80 -j DROP")
    else:
        os.system("iptables -I FORWARD 1 -i " + NETWORK_INTERFACE + " -p tcp --destination-port 80 -j DROP")

def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.hexdigest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

def download_lists(download_date):
    today = str(date.today())

    d1 = datetime.strptime(today, "%Y-%m-%d")
    d2 = datetime.strptime(download_date, "%Y-%m-%d")

    if (d1-d2).days >= 6:
        print("download!")

        easylist = requests.get("https://easylist.to/easylist/easylist.txt", allow_redirects=True)
        open('easylist.txt', 'wb').write(easylist.content)
        EASYLIST = [x.strip() for x in open('easylist.txt', 'r').readlines()]

        pihole = requests.get("https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts", allow_redirects = True)
        open('pihole.txt', 'wb').write(pihole.content)
        PIHOLE = [x.strip() for x in open('pihole.txt', 'r').readlines()]

        return True

def delete_iptables():
    for rule in IPTABLE_RULES:
        os.system(rule)

    IPTABLE_RULES = []

def apply_iptables_rules(blocklist_file):
    for domain in blocklist_file:
        d = domain.strip()
        os.system("iptables -A INPUT -i " + NETWORK_INTERFACE + " -m string --string \"" + d + "\" --algo bm --to 65535 -j DROP")
        os.system("iptables -A OUTPUT -m string --string \"" + d + "\" --algo bm --to 65535 -j DROP")

        IPTABLE_RULES.append("iptables -D INPUT -i " + NETWORK_INTERFACE + " -m string --string \"" + d + "\" --algo bm --to 65535 -j DROP")
        IPTABLE_RULES.append("iptables -D OUTPUT -m string --string \"" + d + "\" --algo bm --to 65535 -j DROP")

def enforce(channel, channel_modality):
    delete_iptables()
    # check modality
    if channel_modality == "noTrack":
        # block only tracking
        blocklist = open("blocklists/" + channel + ".txt", "r")
        apply_iptables_rules(blocklist)
        blocklist.close()

    elif channel_modality == "block":
        # block all traffic from that channel
        os.system("iptables -A INPUT -i " + NETWORK_INTERFACE + " -j DROP")
        IPTABLE_RULES.append("iptables -D INPUT -i " + NETWORK_INTERFACE + " -j DROP")

#TODO: add counter blocked packets
def count_blocked_packets(channel):
    os.system("iptables -L -n -v -x > ./dropped_packets.txt")

    dropped_list = open("dropped_packets.txt", "r").readlines()

    total_dropped = 0

    for line in dropped_list:
        # rules that are set to DROP packets
        if "DROP" in line:
            # take only the number of dropped packets
            dropped_packets = line.split()[0]
            total_dropped += int(dropped_packets)

    print("Total dropped packets is: " + str(total_dropped))

    #update the value of the blocked requests
    try:
        with open('../privacytool/config.json', 'r+') as f:
            data = json.load(f)
            data["blocked_requests"][channel][0] += total_dropped
            f.seek(0)  # rewind
            json.dump(data, f)
            f.truncate()
    except:
        pass

#TODO: actually enforce denylists

def enforce_rules():
        while True:

            hash_and_date = json.load(open('hash_and_dates.json', 'r'))

            if download_lists(hash_and_date['download_date']):
                hash_and_date['download_date'] = str(date.today())
                json.dump(hash_and_date, open('hash_and_dates.json', 'w'))

            current_hash = hash_bytestr_iter(file_as_blockiter(open('config.json', 'rb')), hashlib.sha256())
            if current_hash != hash_and_date['config_hash']:

                # Update hash value in file
                hash_and_date['config_hash'] = current_hash
                json.dump(hash_and_date, open('hash_and_dates.json', 'w'))

                NEW_CONF = {}
                while NEW_CONF == {}:
                # open dashboard configuration if hash is different
                    try:
                        NEW_CONF = json.load(open('config.json', 'r'))
                    except:
                        pass

                # Check HTTP configuration value, if block then all HTTP traffic is dropped
                if NEW_CONF['http_setting'] != OLD_CONF['http_setting']:
                    check_http(NEW_CONF['http_setting'])

                if NEW_CONF['channel_list'][PREVIOUS_CHANNEL] != OLD_CONF['channel_list'][PREVIOUS_CHANNEL]:
                    enforce(CHANNEL_INFO, NEW_CONF['channel_list'][PREVIOUS_CHANNEL])


            if PREVIOUS_CHANNEL and PREVIOUS_CHANNEL != CHANNEL_INFO:
                PREVIOUS_CHANNEL = CHANNEL_INFO

                if NEW_CONF['channel_list'][CHANNEL_INFO] != OLD_CONF['channel_list'][CHANNEL_INFO]:
                    channel_modality = NEW_CONF['channel_list'][CHANNEL_INFO]
                    enforce(CHANNEL_INFO, channel_modality)

            OLD_CONF = NEW_CONF

            if exit_event.is_set():
                break

# Defined what the program should do when exited: remove all iptables rules
exit_event = Event()
def signal_handler(signum, frame):
    #delete all iptables before exiting
    print("Interrupted! Deleting all previous iprules!")
    delete_iptables()
    exit_event.set()

signal.signal(signal.SIGINT, signal_handler)

capture = pyshark.LiveCapture(interface=NETWORK_INTERFACE)

gateway_thread = Thread(target=check_incoming_packets)
gateway_thread.start()

iprules_thread = Thread(target=enforce_rules)
iprules_thread.start()

gateway_thread.join()
iprules_thread.join()
