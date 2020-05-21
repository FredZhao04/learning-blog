本人测试版本: kafka_2.11-2.0.0

一定要先启动ZooKeeper 再启动Kafka 顺序不可以改变。先关闭kafka ，再关闭zookeeper
## 启动zookeeper
`/usr/local/Cellar/zookeeper/3.4.12/bin/zkServer start`
## 启动Kafka
后台常驻方式，带上参数 -daemon，如：
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-server-start.sh -daemon /usr/local/Cellar/kafka_2.11-2.0.0/config/server.properties`
指定 JMX port 端口启动，指定 jmx，可以方便监控 Kafka 集群

`JMX_PORT=9991 /usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-server-start.sh -daemon /usr/local/Cellar/kafka_2.11-2.0.0/config/server.properties`
## 停止Kafka
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-server-stop.sh`
## Topic
### 创建topic
参数 --topic 指定 Topic 名，--partitions 指定分区数，--replication-factor 指定备份数：

`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test`

注意，如果配置文件 server.properties 指定了 Kafka 在 zookeeper 上的目录，则参数也要指定，否则会报无可用的 brokers（下面部分命令也有同样的情况），如：

`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --create --zookeeper localhost:2181/kafka --replication-factor 1 --partitions 1 --topic test`
### 列出所有Topic
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --list --zookeeper localhost:2181`
### 查看 Topic
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test`
### 增加 Topic 的 partition 数
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic test --partitions 5`
### 查看 topic 指定分区 offset 的最大值或最小值
time 为 -1 时表示最大值，为 -2 时表示最小值：
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic test --time -1 --broker-list 127.0.0.1:9092 --partitions 0`
### 删除 Topic
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-topics.sh --zookeeper localhost:2181 --topic test --delete`
### 生产消息
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test`
### 消费信息
#### 从头开始消费
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning`
#### 从尾部开始消费
从尾部开始取数据，必需要指定分区：
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0`
#### 取指定个数
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0 --max-messages 1`
### 消费者Group
#### 指定Group
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test -group test_group --from-beginning
`
#### 消费者Group列表
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list`
#### 查看 Group 详情
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --describe
`
#### 删除 Group 中 Topic
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --topic test --delete
`
#### 删除 Group
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --delete
`
#### 平衡 leader
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-preferred-replica-election.sh --bootstrap-server localhost:9092
`
#### 自带压测工具
`/usr/local/Cellar/kafka_2.11-2.0.0/bin/kafka-producer-perf-test.sh --topic test --num-records 100 --record-size 1 --throughput 100 --producer-props bootstrap.servers=localhost:9092 
`

## Python操作Kafka
### 生产者
```
# -*- coding:utf-8 -*-
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

#handle success
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# handle exception
def on_send_error(excp):
    print('I am an errback')


for i in range(3):
    msg = "msg%d" % i
    #发送的字符串需要转成bytes
    producer.send('test', msg.encode(encoding='utf-8'))\
        .add_callback(on_send_success)\
        .add_errback(on_send_error)

producer.close()
```
### 生产者-压缩消息发送
若消息过大，可压缩消息发送，可选值为 gzip, snappy, lz4。

kafka-python supports gzip compression/decompression natively. To produce or consume lz4 compressed messages, you should install python-lz4 (pip install lz4). To enable snappy compression/decompression install python-snappy (also requires snappy library). 

```
pip install python-snappy
pip install lz4
```
```
# -*- coding:utf-8 -*-
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='lz4')

#handle success
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# handle exception
def on_send_error(excp):
    print('I am an errback')


for i in range(3):
    msg = "msg%d" % i
    #发送的字符串需要转成bytes
    producer.send('test', msg.encode(encoding='utf-8'))\
        .add_callback(on_send_success)\
        .add_errback(on_send_error)

producer.close()
```
### 生产者-json 数据
```
# -*- coding:utf-8 -*-
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m : json.dumps(m).encode(encoding='utf-8'))

#handle success
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# handle exception
def on_send_error(excp):
    print('I am an errback')


for i in range(3):
    msg = "msg%d" % i
    #发送的字符串需要转成bytes
    producer.send('test', {msg: msg})\
        .add_callback(on_send_success)\
        .add_errback(on_send_error)

producer.close()
```
### 消费者
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

for msg in consumer:
    print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))
```
### 消费者-json 数据
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'], value_deserializer=json.loads)

for msg in consumer:
    print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))
    print(msg)
```
### 消费者-读取最早可读消息
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'], value_deserializer=json.loads,
                         auto_offset_reset='earliest')

for msg in consumer:
    print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))
    print(msg)
```
### 消费者-手动设置偏移量
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
from kafka.structs import TopicPartition

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

# 获取test主题的分区信息
print(consumer.partitions_for_topic('test'))
# 获取主题列表
print(consumer.topics())
# 获取当前消费者订阅的主题
print(consumer.subscription())
# 获取当前消费者topic、分区信息
print(consumer.assignment())
# 获取当前主题的最新偏移量
print(consumer.position(TopicPartition(topic='test', partition=0)))
# 重置偏移量，从第1个偏移量消费
consumer.seek(TopicPartition(topic='test', partition=0), 1)
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```
### 订阅多个主题
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])

# 订阅要消费的主题
consumer.subscribe(topics=['test', 'flume'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```
### 消费者-手动拉取消息
```
while True:
    msg = consumer.poll(timeout_ms=5)
    print msg
    time.sleep(1)
```
### 消费者-消息挂起与恢复
```
# -*- coding:utf-8 -*-
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode(encoding='utf-8'))

#handle success
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# handle exception
def on_send_error(excp):
    print('I am an errback')


for i in range(3):
    msg = "msg%d" % i
    data = {
        "message":msg
    }
    #发送的字符串需要转成bytes
    producer.send('test', data)\
        .add_callback(on_send_success)\
        .add_errback(on_send_error)

producer.close()
```
### 消费者组
```
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', group_id='my-group', bootstrap_servers=['localhost:9092'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```
启动多个消费者，消费组可以横向扩展提高处理能力。

