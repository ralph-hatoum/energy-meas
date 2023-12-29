import socket, time
from datetime import datetime, timedelta

throughput = 10 # in messages per second

message_size = 1 # in bytes

test_length = 0.01 # test length in minutes

throughputs = [1, 10, 100, 1000]

message_sizes = [1000, 1000000, 10000000]

def data_sender(throughput, message_size, test_length):

    message = message_size*"a"

    print(f"Will send data at throughput {throughput*message_size} bytes per second")

    start_time = datetime.now() 

    end_time = start_time +timedelta(minutes=test_length)

    print(f"Start time : {start_time}")
    print(f"End time : {end_time}")

    if throughput > 0: 
        while datetime.now() < end_time : 
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 8080))
            data_to_send = "Sample data"
            client_socket.send(data_to_send.encode())
            client_socket.close()
            time.sleep(1/throughput)
    else :
        time.sleep(test_length*60)

    return (start_time,end_time)


def execute_tests(throughputs, message_sizes, test_length):
    test_counter = 0
    results = []
    for throughput in throughputs:
        for message_size in message_sizes :
            if not(throughput == 0 and message_size != 1000):
                print(f"Test #{test_counter} : throughput {throughput} messages per second, message size {message_size} bytes ; equivalent throughput {(throughput*message_size)//1000000} Mb/s")
                result = data_sender(throughput, message_size, test_length)
                start_formatted = result[0].strftime("%Y-%m-%d %H:%M:%S")
                end_formatted = result[1].strftime("%Y-%m-%d %H:%M:%S")
                to_append=(test_counter, start_formatted,end_formatted)
                with open("results.txt", "a") as f:
                    f.write(f"Test #{test_counter} : {throughput} {message_size} {(throughput*message_size)/1000000} \n")
                    f.write(str(start_formatted)+'\n')
                    f.write(str(end_formatted)+'\n')
                    f.write('\n')
                results.append(result)
                test_counter+=1
    print(results)
    return results

execute_tests(throughputs, message_sizes, test_length)

# data_sender(throughput, message_size, test_length)