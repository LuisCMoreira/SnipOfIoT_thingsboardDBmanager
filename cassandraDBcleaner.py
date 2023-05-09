import subprocess
import time

def list_of_keys(key_condition):

    cqlsh_cmd_list = [
        'cqlsh',  # Command to execute cqlsh
        '-e',     # Execute a CQL statement
        f"SELECT DISTINCT entity_type, entity_id, key, partition FROM thingsboard.ts_kv_cf {key_condition};"
    ]

    try:
        output_bytes = subprocess.check_output(cqlsh_cmd_list)
        output_str = output_bytes.decode('utf-8')  # Convert bytes to string
        output_lines = output_str.split('\n')  # Split output into lines
        output_list = [line.split('|') for line in output_lines if line]  # Convert each non-empty line into an array
        #print(output_list)
        return output_list

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Stopping the process")

def time_select():
    while True:
        days_of_del = input("How far back do you whant to keep the data? (days) ")
        time_to_del= int(time.time() * 1000) - (int(days_of_del) * 24 * 60 * 60 * 1000)
        print(f"Will delete data before {days_of_del} days")
        yes_no=input("Is this what you whant?(yes/no)")

        if yes_no.lower()=="yes":
            return time_to_del
        print(" ")

def key_select():
    while True:
        key_to_del=input("Is there a specific key you wish to delete? (input ALL for all data keys) ")

        if len(key_to_del)>3:
            key_condition=f"WHERE key='{key_to_del}' ALLOW FILTERING"
            return key_condition
        else:
            if key_to_del=="ALL":
                key_condition=""
                return key_condition
            else:
                print("Something is wrong, make shore the a selected key name is valid!!!")
                print(" ")

def list_to_delete(output_list, time_to_del, setup_mode):
    if setup_mode:
        print("Database Keys Are:")
    else:
        print("Starting to Delete!")
    num_of_rows = len(output_list)
    # Iterate over each array in the output list
    for array in output_list:

        # Access individual parts of the array
        if len(array)==4 and array[0].replace(" ", "")!="entity_type":
            array_size=len(array)
            entity_type = array[0].replace(" ", "")
            entity_id = array[1].replace(" ", "")
            key = array[2].replace(" ", "")
            partition = array[3].replace(" ", "")
            if len(array) > 4:
                print("something is not ok:")
                print(array)

            if setup_mode:
                print("key: " + key + " -----  entity_id: " + entity_id)

            if not setup_mode:
                cqlsh_cmd_delete = [
                    'cqlsh',  # Command to execute cqlsh
                    '-e',     # Execute a CQL statement
                    f"DELETE FROM thingsboard.ts_kv_cf  WHERE entity_type = '{entity_type}' AND entity_id={entity_id} AND key = '{key}' AND partition= {partition} AND ts < {time_to_del};"
                ]
                output_delete= subprocess.check_output(cqlsh_cmd_delete)
                num_of_rows -= 1

                print(f" Key Set with: Entity Type = {entity_type} and Entity ID = {entity_id} and key = {key} and partition = {partition} Deleted --- {num_of_rows} sets to go" )  # Separator betwee>

setup_mode=True
days_of_del=0
time_to_del=0
key_condition=""


output_list=list_of_keys(key_condition)

list_to_delete(output_list, time_to_del, setup_mode)

time_to_del=time_select()

key_condition=key_select()

output_list=list_of_keys(key_condition)

list_to_delete(output_list, time_to_del, setup_mode)

print(" ")
im_sure = input(f"You will delete all selected data until {time_to_del}, are you sure? (yes/no) ")
if im_sure.lower()=="yes":
    setup_mode=False
else:
   raise SystemExit

list_to_delete(output_list, time_to_del, setup_mode)
