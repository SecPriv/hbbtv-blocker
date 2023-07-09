from genericpath import isdir
import pyshark, os, json

def check_times(filename):
    if '_1' in filename:
        return 'before_consent'
    elif '_2' in filename:
        return 'consent_given'
    elif '_3' in filename:
        return 'consent_revoked'
    else:
        return 'consent_again'

base_folder = '../'

#FORMAT "ip" : ['consent_status']

#There will be a folder for each channel containing the different PCAPS
# the name of the folder is the name of the channel
for folder in os.listdir(base_folder):

    ip_and_time = {}

    for file in os.listdir(base_folder + folder):
    
        if '.pcap' in file:
            try:
                print('Analyzing: ', file)
                cap = pyshark.FileCapture(base_folder + folder + '/' + file, display_filter = 'http or tls')

                for packet in cap:
                    ip = packet.ip.src
                    consent_status = check_times(file)
                    try:
                        if consent_status not in ip_and_time[ip]:
                            ip_and_time[ip].append(consent_status)
                    except:
                        ip_and_time[ip] = [consent_status]
            except:
                print("Error when analyzing:", file)
    
    file_name = folder
    json.dump(ip_and_time, open('../consent_status/' + file_name + '.json', 'w+'))
