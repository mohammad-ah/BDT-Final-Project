#!/usr/bin/python3                                                                                                      
                                                                                                                        
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
from pyspark.streaming.kafka import KafkaUtils                                                                          
                                                                                                                        
def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=['country', 'cases'])                                                
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.cases', format='hive', mode='append')                                       
                                                                                                                        
sc = SparkContext(appName="Something")                                                                                     
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['cases'], {'metadata.broker.list': 'localhost:9092'})                       
                                                                                                                        
lines = ks.map(lambda x: x[1])                                                                                          
                                                                                                                        
transform = lines.map(lambda case: (case, int(len(case.split()))))                                  
                                                                                                                        
transform.foreachRDD(handle_rdd)                                                                                        
                                                                                                                        
ssc.start()                                                                                                             
ssc.awaitTermination()
