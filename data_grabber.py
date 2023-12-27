import requests
import json

sample_request = "https://api.grid5000.fr/stable/sites/lyon/metrics?nodes=taurus-1,taurus-3&metrics=wattmetre_power_watt&start_time=2021-03-21T10:35&end_time=2021-03-21T10:40"

node_name = "taurus-1"

start_time = "2023-12-25T16:54:59.825410"

end_time = "2023-12-25T16:54:59.825410"

request_to_make = f"https://api.grid5000.fr/stable/sites/lyon/metrics?nodes={node_name}&metrics=wattmetre_power_watt&start_time={start_time}&end_time={end_time}"

def timestamps_extractor(file_path):
    timestamps = [[],[],[]]
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for k in range(len(lines)):
        if lines[k][0] == "T":
            split = lines[k].split(" ")
            test_number = split[1]
            message_size = split[10]
            throughput = split[15]
            # print(test_number, message_size, throughput)
            timestamps.append((test_number, message_size, throughput))
        elif lines[k][0] == 'S':
            start_time = lines[k][13:-1]
            timestamps[0].append(start_time)
        elif lines[k][0] == 'E':
            end_time = lines[k][11:-1]
            timestamps[1].append(end_time)
    
    return timestamps

def endpoint_builder(start, end, node_name):
    return f"https://api.grid5000.fr/stable/sites/lyon/metrics?nodes={node_name}&metrics=wattmetre_power_watt&start_time={start}&end_time={end}"


def request_api(timestamps):
    for i in range(len(timestamps[0])):
        start = timestamps[0][i]
        end = timestamps[1][i]
        print(start,end)
        start = format_timestamps(start)
        end = format_timestamps(end)
        endpoint = endpoint_builder(start, end, node_name)
        print(endpoint)
        # response = requests.get(endpoint)
        # print(response)
        # with open(f"test_{i}_results.json","w") as f:
        #     f.write(response.text)

def format_timestamps(timestamp):
    timestamp = timestamp.split(' ')
    timestamp = timestamp[1]
    timestamp = timestamp.split(":")
    timestamp = timestamp[:-1]
    timestamp = ":".join(timestamp)
    print(timestamp)
    return timestamp

def compute_time_difference(t1, t2):
    t1 = t1.split(":")
    t2 = t2.split(":")
    t1, t2 = list(map(int, t1)), list(map(int, t2))
    d1, d2, d3 = t2[0]-t1[0], t2[1]-t1[1], t2[2]-t1[2]

    return d1+d2+d3

def data_parser(json_path):
    with open(json_path) as f:
        data = json.load(f)
    only_energy = []
    timestamp_origin = ""
    for metric in data:
        if metric['metric_id']=='wattmetre_power_watt':
            if timestamp_origin == "":
                timestamp_origin = format_timestamps(metric['timestamp'])
            timestamp = format_timestamps(metric['timestamp'])
            timestamp = compute_time_difference(timestamp_origin, timestamp)
            value = metric['value']
            only_energy.append((timestamp, value))
    return only_energy


timestamps = timestamps_extractor("results.txt")
request_api(timestamps)
# call request_api to request the wattmeters' data
# call data parser to get the energy values with logical timestamps
# write func to make graphs
