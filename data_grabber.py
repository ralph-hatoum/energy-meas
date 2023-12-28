import requests
import json
import matplotlib.pyplot as plt


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
            timestamps[2].append((test_number, message_size, throughput))
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
    file_names = []
    for i in range(len(timestamps[0])):
        start = timestamps[0][i]
        end = timestamps[1][i]
        print(start,end)
        start = format_timestamps(start)
        end = format_timestamps(end)
        endpoint = endpoint_builder(start, end, node_name)
        print(endpoint)
        response = requests.get(endpoint)
        # print(response)
        file_names.append(f"test_{i}_results.json")
        with open(f"test_{i}_results.json","w") as f:
            f.write(response.text)
    return file_names

def format_timestamps(timestamp):
    print(timestamp)
    timestamp = timestamp.split(' ')
    date = timestamp[0]
    time = timestamp[1]
    time = time.split(":")
    time = time[:-1]
    time = ":".join(time)
    timestamp = date+"T"+time
    print(timestamp)
    return timestamp

def compute_time_difference(t1, t2):
    t1 = t1.split(":")
    t2 = t2.split(":")
    t1, t2 = list(map(int, t1)), list(map(int, t2))
    d1, d2, d3 = t2[0]-t1[0], t2[1]-t1[1], t2[2]-t1[2]

    return d1+d2+d3

def format_timestamps_dataparser(timestamp):
    timestamp = timestamp.split("T")
    timestamp = timestamp[1]
    timestamp = timestamp.split("+")
    timestamp = timestamp[0]
    return timestamp

def data_parser(json_path):
    with open(json_path) as f:
        data = json.load(f)
    only_energy = []
    timestamp_origin = ""
    for metric in data:
        if metric['metric_id']=='wattmetre_power_watt':
            if timestamp_origin == "":
                timestamp_origin = format_timestamps_dataparser(metric['timestamp'])
            # print(metric['timestamp'])
            timestamp = format_timestamps_dataparser(metric['timestamp'])
            timestamp = compute_time_difference(timestamp_origin, timestamp)
            value = metric['value']
            only_energy.append((timestamp, value))
    return only_energy

def build_graphs(files, timestamps):
    # print(files)
    test_info = timestamps[2]
    for k in range(len(files)):
        # print(file)
        data = data_parser(files[k])
        X = []
        Y = []
        for element in data:
            X.append(element[0])
            Y.append(element[1])
        plt.figure(figsize=(8, 6))
        plt.plot(X,Y,"x")
        plt.xlabel('Time elapsed in seconds')
        plt.ylabel('Power consumption in Watts')
        plt.title(f'Power consumption during test {test_info[k][0]}, message size {test_info[k][1]}, equivalent throughput {int(test_info[k][1])*int(test_info[k][2])}')
        plt.savefig(files[k]+".png")
        

timestamps = timestamps_extractor("results.txt")
print(timestamps)
# json_names = request_api(timestamps)
build_graphs(["metrics.json"], timestamps)

