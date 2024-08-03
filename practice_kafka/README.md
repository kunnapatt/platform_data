# Repository for test kafka

### Concept of Kafka
#### Feature
- Distributed cluster
- Resilient architecture (replication)
- Fault tolerent
- HC (Horizontal scalability)
- Low latency
#### Use case
- Messaging system
- Activity Tracking
- Log aggregation
- Stream processing

---

### Broker


### Topic
name of topic of publish or subscribe data

### Partition
for each topic divide data to group each group called partition each partition data has sequence and it how to know where current data? answer it has offset for counter data

### Producer
it send data to topic and partition how to send ?
just connect Broker (bootstrap-server) and produce to topic

### Acks
- acks=0 - like udp
- acks=1 - like tcp handshake from leader partition
- acks=all - produce data and waiting until save data to replica

### Consumer
it read data from partition and topic just connect Broker (bootstrap-server)
config on consumer
```
- "bootstrap_server_config": ### where is broker eg. localhost:9092
- "group_id_config": ### group id
- "key_deserializer_class_config": ### output type of key data from consume kafka
- "value_deserializer_class_config": ### output type of value data from consume kafka
- "auto_offset_config_reset": ### offset data it could be 'earliest', 'lastest'
- "enable_auto_commit_config": ### auto count offset 'true', 'false'
```

```
- "poll" - it will pull data if set poll(1000) will waiting 1 sec for timeout and return value pull
```
####  Consumer group
if system produce a lot of data but consumer side not enough for consume can immediately scale consume. and has rule for consumer group cann't more than number of partition in topic


### Order
consumer side read data order it already just partition level only it data has a sequence should design order on message key

### Zookeeper
- managing brokers
- tracking topic, partitions
- select leader, replica of partitions
- send signal to kafka when event
- save producer, consumer each should how limit read, write
- Authorization user on topic
- save consumer group and tracking offset

---

## Step to build
1). download and extract scala version [link](https://kafka.apache.org/downloads)

2). go to path extract kafka

3). Start zookeeper server
```
## Should to uncomment in file 'config/zookeeper.properties'

dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=0
admin.enableServer=false

```
and start zookeeper server
```
> bin/zookeeper-server-start.sh config/zookeeper.properties
```

4). Start server
```
> bin/kafka-server-start.sh config/server.properties
```

### Optional

#### Create topic
```
> bin/kafka-topic.sh --create --bootstrap-server localhost:2181 \
--replication-factor <number_of_replication> \
--partitions <number_of_partition> \
--topic <name_of_topic>
```

#### Describe topic
```
> bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic <name_of_topic>
```