import urllib.request
from bs4 import BeautifulSoup
import json

def main():
    nodes = []
    links = []

    # http://www.sangiin.go.jp/japanese/san60/s60_shiryou/giinsuu_kaiha.htm
    html = urllib.request.urlopen("http://www.sangiin.go.jp/japanese/san60/s60_shiryou/giinsuu_kaiha.htm")
    soup = BeautifulSoup(html, features="html.parser")
    tables = soup.find_all("table")

    table_index = 0
    td_index = 0

    current_tr_nodes = []

    for table in tables:
        first_tr = table.find_all("tr")[2]
        tds = first_tr.find_all("td")

        prev_tr_nodes = current_tr_nodes[:]
        current_tr_nodes.clear()
        for td in tds:
            if td.has_attr("headers") and table_index >= 19:
                print(td.text)

                stem = td["headers"][0].split('-')[-2]
                num_senkyo = td["headers"][0].split('-')[-1]
                print(stem)

                node = {}
                node["node"] = str(td_index)
                node["name"] = str(td["headers"][0])
                node["stem"] = stem
                node["seats"] = int(td.text)

                nodes.append(node)
                current_tr_nodes.append(node)

                for prev_node in prev_tr_nodes:
                    if prev_node["stem"] == node["stem"]:
                        link = {}
                        link["source"] = prev_node["node"]
                        link["target"] = node["node"]
                        link["value"] = node["seats"]

                        links.append(link)
                td_index = td_index + 1

        prev_tr = td
        table_index = table_index + 1

    print(nodes)
    print(links)

    json_object = {}
    json_object["nodes"] = nodes
    json_object["links"] = links

    fw = open('output_seat.json', 'w', encoding="utf-8")
    json.dump(json_object, fw, indent=4, ensure_ascii=False)
    return

if __name__ == '__main__':
    main()
