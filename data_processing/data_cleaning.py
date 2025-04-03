from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("DataCleaning") \
    .getOrCreate()

# Load raw data from Kafka or CSV
raw_data = spark.read.json("data/real_time_data.json")

# Handle Missing Values: Fill with median or remove rows
cleaned_data = raw_data.fillna({"value": raw_data.approxQuantile("value", [0.5], 0.25)[0]})

# Handle Outliers: Example of Z-Score Filtering
mean = cleaned_data.select("value").agg({"value": "mean"}).collect()[0][0]
stddev = cleaned_data.select("value").agg({"value": "stddev"}).collect()[0][0]

cleaned_data = cleaned_data.filter((col("value") > mean - 3*stddev) & (col("value") < mean + 3*stddev))

# Remove duplicates
cleaned_data = cleaned_data.dropDuplicates()

# Show the cleaned data for verification
cleaned_data.show()

# Save cleaned data for further processing (e.g., Snowflake)
cleaned_data.write.parquet("processed_data.parquet")

print("✅ Data cleaning complete!")
