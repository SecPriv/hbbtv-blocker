from django.http import HttpResponse
from django.shortcuts import render
import json
import os

configuration_file = open("./config.json", "r")
json_config = json.load(configuration_file)
configuration_file.close()

def set_config_http(http_value):
    configuration_file = open("./config.json", "w")
    if http_value == 'allow_http':
        print("allow http")
        json_config["http_setting"] = "allow"
    else:
        print("block http")
        json_config["http_setting"] = "block"
    json.dump(json_config, configuration_file)
    configuration_file.close()

def set_config_channels(broadcaster, mode):
    configuration_file = open("./config.json", "w")

    json_config['channel_list'][broadcaster] = mode

    json.dump(json_config, configuration_file)
    configuration_file.close()

def set_default_config(default_config_value):

    if default_config_value == 'default_on':
        configuration_file = open("./config.json", "w")

        for channel, mode in json_config['channel_list'].items():
            json_config['channel_list'][channel] = 'noTrack'
        
        json_config["http_setting"] = "block"

        json.dump(json_config, configuration_file)
        configuration_file.close()

#add new rule for new domain added in blocklist page
def new_iprule(domain):
    print("New iprule added for " + domain)
    os.system("iptables -A INPUT -i enx00e04c6945bb -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP")

#remove rule previously added in blocklist page
def delete_iprule(domain):
    print("Iprule deleted for " + domain)
    os.system("iptables -D INPUT -i enx00e04c6945bb -m string --string \"" + domain + "\" --algo bm --to 65535 -j DROP")

def index(request):

    body = {}

    #decode payload of post request and convert it into JSON format
    try:
        my_json = request.body.decode('utf8').replace("'", '"')
        body = json.loads(my_json)
    except:
        pass

    #set value of http settings in the JSON configuration file
    if ("http_settings" in body):
        set_config_http(body['http_settings'])
    
    #set value of broadcaster traffic modality in JSON configuration file
    if ("broadcaster" in body):
        set_config_channels(body['broadcaster'], body['modality'])

    if "default_config_value" in body:
        set_default_config(body['default_config_value'])

    context = {}

    #read those values from the json config file (both for the plot and for the configuration)
    context['previous_config'] = json_config['channel_list']
    context['http_config'] = json_config['http_setting']

    conf_file = open("./config.json", "r")
    json_plot_data = json.load(conf_file)
    conf_file.close()

    context['plot_data'] = json_plot_data['blocked_requests']

    return render(request, "configDashboard/index.html", context)

def blocklist(request):

    body = {}

    #decode payload of post request and convert it into JSON format
    try:
        my_json = request.body.decode('utf8').replace("'", '"')
        body = json.loads(my_json)
    except:
        pass

    #add new iptables rule for customized domains
    if ("domain" in body):
        new_iprule(body["domain"])

    if("domain_delete" in body):
        delete_iprule(body["domain_delete"])

    return render(request, "configDashboard/blocklist.html")

def about(request):
    print("About")
    return render(request, "configDashboard/about.html")