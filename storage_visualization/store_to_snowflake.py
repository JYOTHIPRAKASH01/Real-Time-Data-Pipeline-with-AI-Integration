import snowflake.connector
import pandas as pd

# Snowflake connection configuration
conn = snowflake.connector.connect(
    user='<your_snowflake_user>',
    password='<your_snowflake_password>',
    account='<your_snowflake_account>',
    warehouse='COMPUTE_WH',
    database='REAL_TIME_DB',
    schema='PUBLIC'
)

# Example data to store (replace with processed data)
data = {
    "sensor_id": [1, 2, 3],
    "temperature": [22.5, 23.1, 24.0],
    "humidity": [60, 55, 58],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Store the data in Snowflake
for index, row in df.iterrows():
    query = f"""
    INSERT INTO REAL_TIME_TABLE (sensor_id, temperature, humidity)
    VALUES ({row['sensor_id']}, {row['temperature']}, {row['humidity']})
    """
    conn.cursor().execute(query)

print("Data successfully stored in Snowflake!")
