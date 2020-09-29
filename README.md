# BDT-Final-Project

Please find a description and a demo in thie link:
### Video [here] (https://youtu.be/7UzZhkg8TYo)


You can find all the steps in the link above, in addition to how to run the scripts.

# Kafka - Spark Streaming - Hive


This is an example of building a Proof-of-concept for Kafka + Spark streaming with Hive. 

We will 
* create a stream of cases(COV-19) that will be sent to a Kafka queue
* pull the cases from the Kafka cluster
* calculate the cases for each case
* save this data to a Hive table

To do this, we are going to set up an environment that includes 
* a single-node Kafka cluster
* a single-node Hadoop cluster
* Hive and Spark

---
## 1. Install Kafka for Python

Make sure you have `Python3` is installed and accessible with `python3`, also install `pip3` then

``` bash
~$ pip3 install kakfa-python 
```

Confirm this installation with 

``` bash
~$ pip3 list | grep kafka
```
---
## 2. Hive Table

Make the database for storing our cases data:

``` bash
hive> CREATE TABLE cases (country STRING, cases INT)
    > ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|'
    > STORED AS TEXTFILE;
```

You can use `SHOW TABLES;` to double check that the table was created.

---
## 3. Install PySpark

Make sure Scala is installed on your system.
Test with 
```bash
~$ scala -version
```
If not run the command

```bash
~$ sudo apt install scala -y
```


We will need `pyspark`.

``` bash
~$ pip3 install pyspark
```

Check with
```bash
~$ pip3 list | grep spark
```

Now let's add the Spark /bin files to the path, open up `.bashrc` and add the following
```bash
export PATH=$PATH:/home/<USER>/spark/bin
export PYSPARK_PYTHON=python3
```

By setting the `PYSPARK_PYTHON` variable, we can use PySpark with Python3, the version of Python we have been using so far.


We also need a JAR file that isn't included in PySpark, it will allow us to connect to Kafka and use KafkaUtils.
Download the JAR file from [search.maven.org](https://search.maven.org/search?q=a:spark-streaming-kafka-0-8-assembly_2.11).


---
## 4. About the Code

### Stream Producer

We have two options

* #### OPTION 1
    Using external API's such as Tiwtter, Facebook, Amazon...

* #### OPTION 2
    Using and simulating "fake cases generator". Which is included in the file `fake_stream.py`. 

    I added a file containing all the countries in the world, in which they will be used to generate random cases in random countries.

### Stream Consumer + Spark Transformer

The file `transformer.py` is handling it.  

---
## 5. Running our demo

Now we are ready to run the demo.

---
* ### 1 Zookeeper

In your first terminal tab start a Zookeeper instance. This is required for running a Kafka cluster

```bash
~$ cd kafka/ #where ever it exists on your system
~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

Keep all the processes running, and open a new terminal tab for each step.

---
* ### 2 Kafka Broker

Now let's start the Kafka broker.

```bash
~$ cd kafka/
~/kafka$ bin/kafka-server-start.sh config/server.properties
```

---
* ### 3 Create Kafka Topic

Now let's create the topic that will hold our cases.

First check if any topics exist on the broker

```bash
~/kafka$ bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Now make a new topic named `cases`

```bash
~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic cases
```

Run the `--list` command from above to make sure the `cases` topic was successfully created.


---
* ### 4 Hive Metastore

``` bash
~$ hive --services metastore
```

---
* ### 5 Hive


```bash
~$ hive

 ...

hive> use default;
hive> select count(*) from cases;
```

---
* ### 6 Stream Producer

Run the stream producer. 

```bash
~$ ./fake_stream.py
```

This script will produce output everytime a case is generated and sent to the Kafka cluste.

---
* ### 7 Stream Consumer + Spark Transformer

Now we are ready to run the consumer.
```bash
~$ spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar transformer.py
```
And this should be it

---

