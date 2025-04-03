from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.streaming import DataStreamWriter

KAFKA_TOPIC = "real_time_data"
KAFKA_BROKER = "localhost:9092"

# Define Spark Session
spark = SparkSession.builder \
    .appName("RealTimeDataProcessing") \
    .getOrCreate()

# Define Schema
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("sensor_id", StringType(), True),
    StructField("value", DoubleType(), True)
])

# Read data from Kafka
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Deserialize JSON
processed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to Console (for debugging)
query = processed_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
