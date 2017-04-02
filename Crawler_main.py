import urllib.request
import pickle
import json
import numpy as np


def crawler():
    url = "https://www.worldbaseballclassic.com/lookup/json/named.wbc_leader_pitching.bam"
    parms = {
        'season': '2017',
        'sort_order': 'asc',
        'stat': 'era',
        'qualifies': 'N'
    }
    q = urllib.parse.urlencode(parms)

    json_content = json.loads(urllib.request.urlopen("{}?{}".format(url, q)).read().decode('utf-8'))
    picked_data = json_content['wbc_leader_pitching']['queryResults']['row']
    processed_data = json_to_numpy_parser(picked_data)
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    print(processed_data)

    save_as_pickle('wbc_pitcher_stats.pickle', processed_data)


def json_to_numpy_parser(json_data):
    processed_data = []
    table_head = []
    # retrieve table head
    for key, value in json_data[0].items():
        table_head.append(key)
    processed_data.append(table_head)
    # setup json format data
    for element in json_data:
        local_data = []
        for key, value in element.items():
            local_data.append(value)
        processed_data.append(local_data)

    return np.array(processed_data)


def save_as_pickle(dest_path, data):
    with open(dest_path, 'wb') as f:
        pickle.dump(data, f)
    f.closed


def save_as_text(dest_path, data):
    with open(dest_path, 'a') as f:
        for element in data:
            f.write(''.join(element))
    f.closed

if __name__ == '__main__':
    crawler()
