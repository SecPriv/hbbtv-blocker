from genericpath import isdir
import pyshark, os, json

def check_times(time):
    if time < 1200:
        return 'before_consent'
    elif time < 3600:
        return 'consent_given'
    elif time < 4500:
        return 'consent_revoked'
    else:
        return 'consent_again'

base_folder = '../'

#FORMAT "ip" : ['consent_status']

for file in os.listdir(base_folder):
    
    ip_and_time = {}
    
    if '.pcap' in file:
        try:
            print('Analyzing: ', file)
            cap = pyshark.FileCapture(base_folder + file, display_filter = 'http or tls')

            for packet in cap:
                time = packet.frame_info.time_relative
                ip = packet.ip.src
                consent_status = check_times(float(time))
                try:
                    if consent_status not in ip_and_time[ip]:
                        ip_and_time[ip].append(consent_status)
                except:
                    ip_and_time[ip] = [consent_status]
        except:
            print("Error when analyzing:", file)
    
        file_name = file.strip('.pcapng')
        json.dump(ip_and_time, open('../consent_status/' + file_name + '.json', 'w+'))
