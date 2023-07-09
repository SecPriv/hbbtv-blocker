import subprocess, json
from time import sleep

results_no_pihole = {}

urls = ['http://hbbtv.rds.radio', 'https://ht.la7.it/index.php', 'http://discovery.castoola.tv/realtime']

for url in urls:

    print('Analyzing: ', url)

    results_no_pihole[url] = []

    for i in range(0,100):

        if i % 10 == 0:
            print('Got ', i, ' packets')

        command = "curl -so /dev/null -w '%{time_total}\n' " + urls[0]
        out = subprocess.run([command], stdout=subprocess.PIPE, shell=True)

        time = float((out.stdout).decode("utf-8").strip('\n'))

        results_no_pihole[url].append(time)

        sleep(1)

print(results_no_pihole)
json.dump(results_no_pihole, open('./results_with_pi.json', 'w'))


    