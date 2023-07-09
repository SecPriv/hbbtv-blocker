import json
from statistics import mean, stdev
import pyshark, os
from time import sleep

def compute_recurrency(times, host, occurrencies, frequencies):

    frequencies[host] = {}

    avg = mean(times)
    st_dev = stdev(times)

    frequencies[host]['occurrencies'] = occurrencies
    frequencies[host]['average'] = avg
    frequencies[host]['stdev'] = st_dev

    #print("\n\nDomain: " + host + ", Occurrencies: " + str(occurrencies))
    #print("The average elapsing time between requests is " + str(avg) + " seconds")
    #print("The standard deviation between requests is " + str(st_dev) + " seconds")
    return 0

def compute_difference(times):
    time_diff = []
    for i in range(len(times) - 1):
        time_diff.append(times[i+1] - times[i])

    return time_diff

base_folder = '../martina_traffic/'


for folder in os.listdir(base_folder):
    
    domains_and_times = {}

    print(folder)

    try:
        dns_map = json.load(open(base_folder + '/results/dns_mapping/' + folder + '.json', 'r'))
    except:
        pass

    
    for file in os.listdir(base_folder + folder):
    
        if '.pcap' in file:
            try:
                print('Analyzing: ', file)
                cap = pyshark.FileCapture(base_folder + folder + '/' + file, display_filter = 'http or tls')

                sleep(2)

                for packet in cap:

                    time = float(packet.frame_info.time_relative)
                    ip = packet.ip.src

                    try:
                        try:
                            domains_and_times[dns_map[ip]].append(time)
                        except:
                            domains_and_times[ip].append(time)
                    except:
                        try:
                            domains_and_times[dns_map[ip]] = [time]
                        except:
                            domains_and_times[ip] = [time]

                sleep (4)
            except:
                print("Error when analyzing:", file)

    frequencies = {}

    for domain, times in domains_and_times.items():
        #number of occurrencies must be bigger than a treshold
        if len(times) > 10:
            time_diff = compute_difference(times)
            compute_recurrency(time_diff, domain, len(times), frequencies)

    json.dump(frequencies, open(base_folder + folder + '_frequencies.json', 'w'))
