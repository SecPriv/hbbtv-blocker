from genericpath import isdir
import pyshark, os, json

base_folder = '../'

#There will be a folder for each channel containing the different PCAPS
# the name of the folder is the name of the channel
for folder in os.listdir(base_folder):

    dns_map = {}

    for file in os.listdir(base_folder + folder):
        
        if '.pcap' in file:
            try:
                print('Analyzing: ', file)
                cap = pyshark.FileCapture(base_folder + folder + '/' + file, display_filter = 'dns.flags.response == 1')

                for packet in cap:
                    try:
                        dns_map[packet.dns.a] = packet.dns.qry_name
                    except:
                        pass
            except:
                print("Error when analyzing:", file)
        
    file_name = folder
    json.dump(dns_map, open('../dns_mapping/' + file_name + '.json', 'w+'))
