from genericpath import isdir
import pyshark, os, json

base_folder = '../'

for file in os.listdir(base_folder):

    dns_map = {}
    
    if '.pcap' in file:
        try:
            print('Analyzing: ', file)
            cap = pyshark.FileCapture(base_folder + file, display_filter = 'dns.flags.response == 1')

            for packet in cap:
                try:
                    dns_map[packet.dns.a] = packet.dns.qry_name
                except:
                    pass
        except:
            print("Error when analyzing:", file)
    
        file_name = file.strip('.pcapng')
        json.dump(dns_map, open('../dns_mapping/' + file_name + '.json', 'w+'))
