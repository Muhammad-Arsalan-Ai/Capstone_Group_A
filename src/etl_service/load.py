import redis
import json
from transform import calculate_average

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# Calculate the average, group by specialization, and sort by specialization
average_df = calculate_average()

average_df_json = average_df.toJSON().collect()

# Set the JSON string as the value in Redis
r.set('average_data', json.dumps(average_df_json))

# print(r.get('average_data'))