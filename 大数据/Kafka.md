##kafka分布式的情况下，如何保证消息的顺序?
Apache Kafka官方保证了partition内部的数据有效性（追加写、offset读）；为了提高Topic的并发吞吐能力，可以提高Topic的partition数，并通过设置partition的replica来保证数据高可靠；但是在多个Partition时，不能保证Topic级别的数据有序性。因此，如果你们就像死磕kafka，但是对数据有序性有严格要求，那我建议：创建Topic只指定1个partition，这样的坏处就是磨灭了kafka最优秀的特性。所以可以思考下是不是技术选型有问题， kafka本身适合与流式大数据量，要求高吞吐，对数据有序性要求不严格的场景。
###局部顺序
其实在大部分业务场景下，只需要保证消息局部有序即可，什么是局部有序？局部有序是指在某个业务功能场景下保证消息的发送和接收顺序是一致的。如：订单场景，要求订单的创建、付款、发货、收货、完成消息在同一订单下是有序发生的，即消费者在接收消息时需要保证在接收到订单发货前一定收到了订单创建和付款消息。

针对这种场景的处理思路是：针对部分消息有序（message.key相同的message要保证消费顺序）场景，可以在producer往kafka插入数据时控制，同一key分发到同一partition上面。因为每个partition是固定分配给某个消费者线程进行消费的，所以对于在同一个分区的消息来说，是严格有序的（在kafka 0.10.x以前的版本中，kafka因消费者重启或者宕机可能会导致分区的重新分配消费，可能会导致乱序的发生，0.10.x版本进行了优化，减少重新分配的可能性）。

##kafka复习知识点
https://blog.csdn.net/m0_37847176/article/details/80015328

https://blog.csdn.net/z69183787/article/details/79895721

##发现kafka丢消息后的排查
https://www.jianshu.com/p/ec93eb4f7733

https://blog.csdn.net/qq_33160722/article/details/52903380
##启动zookeeper
```
cd /usr/local/Cellar/zookeeper-3.4.11/bin

sh zkServer.sh start
```

##启动Kafka
```
cd /usr/local/Cellar/kafka_2.11-0.10.2.1/

//启动kafka
sh bin/kafka-server-start.sh config/server.properties &

cd bin

//其中kafkatopic是topic的名称
sh kafka-topics.sh --create --topic kafkatopic --replication-factor 1 --partitions 1 --zookeeper localhost:2181

//列示所有的topic
sh *kafka-topics.sh --list --zookeeper localhost:2181*

//列示指定topic的详细信息
sh kafka-topics.sh --describe --topic kafkatopic --zookeeper localhost:2181

//启动生产者
sh kafka-console-producer.sh --broker-list localhost:9092 --sync --topic kafkatopic

//启动消费者
sh kafka-console-consumer.sh --zookeeper localhost:2181 --topic kafkatopic --from-beginning
```

##启动redis
```
cd /usr/local/Cellar/bin

redis-server redis.conf &

//如果想连接特定的ip
redis cli -h 192.168.11.62
```
##mac查看端口占用情况
命令 lsof -i tcp:port  （port替换成端口号，比如6379）可以查看该端口被什么程序占用，并显示PID，方便KILL

##实时监控文件
```
//删掉之后再创建无法监控
tail -f 文件名
//删掉之后再创建可以持续监控
tail -F 文件名
```

##启动flume采集数据
cd /usr/local/Cellar/apache-flume-1.8.0-bin

```
bin/flume-ng agent -c conf -f /Users/fred/Documents/myconf/spooldir-kafka.properties -n a1 -Dflume.root.logger=INFO,console
```
-c conf   指定flume自身的配置文件所在目录
-f /Users/fred/Documents/myconf/spooldir-kafka.properties  指定我们所描述的采集方案
-n a1  指定我们这个agent的名字

