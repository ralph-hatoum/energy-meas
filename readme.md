# Energy consumption measurements on Grid5000

This repository is dedicated to making energy consumption measurements on Grid5000. 

## Goal
My main goal is to measure the energy overhead incurred by sending segments over TCP, opposed to simply having the machine on but idle. I also used this project as a first experience running jobs on Grid5000.

## Experiments performed 
I reserved two nodes and ran a server on one of them and a client on another.

The server is a simple TCP server that listens to connections, receieves messages and displays them. For the sake of this experiment, the server part is not really important, we only need it to be listening and open to connections. 

On the client, we succintly send messages of different sizes at different throughputs :

|           | Test 0 | Test 1 | Test 2 | Test 3 | Test 4 | Test 5 | Test 6|  Test 7|
|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| Message size (Bytes) |   | 1000 | 1000000 | 10000000 | 1000 | 1000000 | 10000000 | 1000 |
| Message throughput (msg/sec) |   | 1 | 1 | 1 | 10 | 10 | 10 | 100
| Throughput (Mb/sec) |  0 | 0.001 | 1 | 10 | 0.1 | 10 | 100 | 0.1

For each test, we traffic for 5 consecutive minutes. Energy consumption of machines in the Grid5000 cluster is monitored through physical wattmeters that make measures every second. 

On each test, we write down the times of start and end of our test. After all tests are done, we retrieve the measurements through an API call. We present in graphs the variation of energy consumption over the duration of the test, as well as the mean energy consumption over the duration of the test.

## Results

Here are a few graphs (all graphs are in the graphs directory, and all raw measures in the results directory) : 

![Energy consumption with no traffic](./graphs/test_0_results.json.png)

![Energy consumption with no traffic](./graphs/test_2_results.json.png)

![Energy consumption with no traffic](./graphs/test_5_results.json.png)


There does not seem to be a spike in power consumption as traffic load increases.

## To work on

TODO explain why 5 minutes, why the throughputs
There are mistakes in the graphs titles regarding the throughputs



