import os, json, hashlib, requests
from datetime import date, datetime

active_iptables_rules = []

# run with sudo



def iptables_rule(domain):
    os.system("iptables -A INPUT -i enx00e04c6945bb -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP")
    os.system("iptables -A OUTPUT -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP")
    rule_to_delete = "iptables -D INPUT -i enx00e04c6945bb -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP"
    active_iptables_rules.append(rule_to_delete)
    rule_to_delete = "iptables -D OUTPUT -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP"
    active_iptables_rules.append(rule_to_delete)
    #print("iptables -A INPUT -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP")

# delete the activated iptable rules
def delete_iptables():
    print("Deleting iptables")
    for item in active_iptables_rules:
        os.system(item)


def enforce_rules(blocklist_file):
    for domain in blocklist_file:
        iptables_rule(domain.strip())


def count_blocked_packets(channel, config):
    os.system("iptables -L -n -v -x > ./dropped_packets.txt")

    dropped_file = open("dropped_packets.txt", "r")
    dropped_list = dropped_file.readlines()

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


def check_http(http_value):
    if http_value == "allow":
        os.system("iptables -D FORWARD -i enx00e04c6945bb -p tcp --destination-port 80 -j DROP")
    else:
        os.system("iptables -I FORWARD 1 -i enx00e04c6945bb -p tcp --destination-port 80 -j DROP")


def enforce(channel, channel_modality):
    # check modality
    if channel_modality == "allow":
        # allow all traffic
        print("Allow all Traffic of channel: " + channel)

    elif channel_modality == "noTrack":
        # block only tracking + load blocklist
        print("Block Tracking of channel: " + channel)
        blocklist_name = "blocklists/" + channel + ".txt"
        blocklist = open(blocklist_name, "r")
        enforce_rules(blocklist)
        blocklist.close()

    elif channel_modality == "block":
        # block all traffic from that channel
        os.system("iptables -A INPUT -i enx00e04c6945bb -j DROP")
        active_iptables_rules.append("iptables -D INPUT -i enx00e04c6945bb -j DROP")
        print("Block all Traffic of channel: " + channel)

#used to set first parameters
first = True

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

        pihole = requests.get("https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts", allow_redirects = True)
        open('pihole.txt', 'wb').write(pihole.content)

        return True


try:
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

            # open dashboard configuration if hash is different
            try:
                conf_file = json.load(open('config.json', 'r'))
            except:
                conf = {}

        break



#         # check which channel is being watched
#         try:
#             channel_file = open("channel.txt", "r")
#             channel = channel_file.readline().strip()
#             channel_file.close()
#         except:
#             channel = ""

#         if len(conf) == 0 or channel == "":
#             pass
#         else:
#             channel_list = conf["channel_list"]

#             # check modality that is enforced
#             channel_modality = channel_list[channel]

#             #check whether HTTP is allowed or not
#             http_setting = conf["http_setting"]

#             #update initial parameters and enforce modality
#             if first:
#                 channel_old = channel
#                 channel_modality_old = channel_modality
#                 enforce(channel, channel_modality)
#                 http_setting_old = http_setting
#                 first = False

#             #if http settings have changed, add the specific iprule
#             if http_setting != http_setting_old:
#                 check_http(http_setting)
#                 http_setting_old = http_setting

#             # if something has changed change iprules, otherwise not
#             if channel != channel_old or channel_modality != channel_modality_old:
#                 print("Something has changed!")

#                 #TODO: check if this works
#                 count_blocked_packets(channel_old, conf)

#                 # delete the previous rules
#                 delete_iptables()

#                 # empty the list of the active rules
#                 active_iptables_rules = []

#                 #enforce the right modality
#                 enforce(channel, channel_modality)

#                 # update parameters
#                 channel_old = channel
#                 channel_modality_old = channel_modality
except KeyboardInterrupt:
    #delete all iptables before exiting
    # delete_iptables()
    print("Interrupted! Deleting all previous iprules")
