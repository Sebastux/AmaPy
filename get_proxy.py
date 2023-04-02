import pandas as pd
import requests

url = "https://free-proxy-list.net/"
url_site = "https://books.toscrape.com/"
good_proxies = []

reponse = requests.get(url)

list_column = ['Code', 'Country', "Anonymity", "Google", "Last Checked", 'Https']
proxy_list = pd.read_html(reponse.text)[0]
filtered_proxy_list = proxy_list.loc[proxy_list['Https'] == "yes"].drop(list_column, axis=1).reset_index(drop=True)

print(f"taille : {len(filtered_proxy_list)}")
for idx in range(len(filtered_proxy_list)):
    proxies = {'http': f'{filtered_proxy_list["IP Address"][idx]}:{filtered_proxy_list["Port"][idx]}',
               'https': f'{filtered_proxy_list["IP Address"][idx]}:{filtered_proxy_list["Port"][idx]}',
              }
    print(proxies)
    try:
        response = requests.get(url_site, proxies=proxies, timeout=5)
        print(f"Numéro : {idx}, réponse : {response.status_code}")
        if response.status_code == 200:
            good_proxies.append(f'{filtered_proxy_list["IP Address"][idx]}:{filtered_proxy_list["Port"][idx]}')
            print("OK")
    except:
        pass
print(good_proxies)
print(len(good_proxies))

with open("/home/Sebastien/Dépots/privé/TestJupyter/proxy_list.txt", "wt", encoding="utf-8") as f:
    for i in range(len(good_proxies)):
        f.write(f"{good_proxies[i]}\n")