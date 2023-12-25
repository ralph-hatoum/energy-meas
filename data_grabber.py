import requests
import json

sample_request = "https://api.grid5000.fr/stable/sites/lyon/metrics?nodes=taurus-1,taurus-3&metrics=wattmetre_power_watt&start_time=2021-03-21T10:35&end_time=2021-03-21T10:40"

node_name = "taurus-1"

start_time = "2023-12-25T16:54:59.825410"

end_time = "2023-12-25T16:54:59.825410"

request_to_make = f"https://api.grid5000.fr/stable/sites/lyon/metrics?nodes={node_name}&metrics=wattmetre_power_watt&start_time={start_time}&end_time={end_time}"

def timestamps_extractor(file_path):
    timestamps = [[],[]]
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line[0] == 'S':
            start_time = line[13:-1]
            timestamps[0].append(start_time)
        elif line[0] == 'E':
            end_time = line[11:-1]
            timestamps[1].append(end_time)
    
    return timestamps

def endpoint_builder(start, end, node_name):
    return f"https://api.grid5000.fr/stable/sites/lyon/metrics?nodes={node_name}&metrics=wattmetre_power_watt&start_time={start}&end_time={end}"


def request_api(timestamps):
    for i in range(len(timestamps[0])):
        start = timestamps[0][i]
        end = timestamps[1][i]

    endpoint = endpoint_builder(start, end, node_name)
    response = requests.get(endpoint)

def format_timestamps(timestamp):
    timestamp = timestamp.split('T')
    timestamp = timestamp[1]
    timestamp = timestamp.split("+")
    timestamp = timestamp[0]
    return timestamp

def data_parser(json_path):
    with open(json_path) as f:
        data = json.load(f)
    only_energy = []
    for metric in data:
        if metric['metric_id']=='wattmetre_power_watt':
            timestamp = metric['timestamp']
            value = metric['value']
            only_energy.append((timestamp, value))
    print(only_energy)

        
format_timestamps("2023-12-25T20:52:24+01:00")
# data_parser("metrics.json")
# endpoint = endpoint_builder("2023-12-25T16:54", "2023-12-25T16:56", "orion-1")
# print(endpoint)