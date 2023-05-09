import subprocess
from datetime import datetime

timestamp = datetime.now()
date=timestamp.date()
print(date)

cqlsh_cmd_ts_kv_partitions_cf = [
    'cqlsh',  # Command to execute cqlsh
    '-e',     # Execute a CQL statement
    f"COPY thingsboard.ts_kv_partitions_cf TO './{date}_ts_kv_partitions_cf.csv' WITH HEADER = true AND DELIMITER = ',' AND QUOTE = '\"'"
]

cqlsh_cmd_ts_kv_cf = [
    'cqlsh',  # Command to execute cqlsh
    '-e',     # Execute a CQL statement
    f"COPY thingsboard.ts_kv_cf TO './{date}_ts_kv_cf.csv' WITH HEADER = true AND DELIMITER = ',' AND QUOTE = '\"'"
]

try:
    output = subprocess.check_output(cqlsh_cmd_ts_kv_partitions_cf)
    print(output)
    print(f"{date}_ts_kv_partitions_cf")
    output = subprocess.check_output(cqlsh_cmd_ts_kv_cf)
    print(f"{date}_ts_kv_cf")
    #print(output)
except subprocess.CalledProcessError as e:
    print("Error:", e)
