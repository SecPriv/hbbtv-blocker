import json

occurrences_domains = {}

files = ['rai', 'rds', 'rtl', 'bom', 'la7', 'mediaset', 'radiokisskiss', 'radioliberta', 'nove', 'realtime', 'sportitalia', 'twentyseven_mediaset']

to_exclude = ['10.42.0.124', 'it.tv.global.mi.com', '10.42.0.147', 'clients3.google.com', 'ichnaea.netflix.com', 'api-global.netflix.com', 
    'cdn.alsgp0.fds.api.mi-img.com', 'app-measurement.com', 'firebaseinstallations.googleapis.com', 'connectivitycheck.gstatic.com',    
    'play.googleapis.com', 'data.mistat.intl.xiaomi.com', 'es.tv.global.mi.com', 'cdn.awsde0-fusion.fds.api.mi-img.com', 'mtalk.google.com', 
    'mitv.tracking.intl.miui.com', 'nrdp.prod.cloud.netflix.com', 'www.gstatic.com', 'android-safebrowsing.google.com', 
    'antv-28-xiaomi-mitvmssp2-412001200.api.amazonvideo.com', 'assets.androidtv.com', 'play-fe.googleapis.com']

for file in files:

    before_consent = []

    full_analysis = json.load(open('../full_analysis/' + file + '.json', 'r'))

    for domain,value in full_analysis.items():

        if 'before_consent' in value['consent_status'] and domain not in to_exclude:
            if 'netflix' not in domain and 'amazonvideo' not in domain:
                before_consent.append(domain)

    json.dump(before_consent, open('../full_analysis/domains_before_consent/' + file + '.json', 'w+'))
