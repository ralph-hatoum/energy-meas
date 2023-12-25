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

timestamps = timestamps_extractor("./results.txt")
print(timestamps)