import json

import pandas as pd
from load_data import filter_data, filter_data, load_auth, load_process, load_redteam
import os

# def filter_auth(df):
#     # Remove machine accounts
#     df = df[~df.src_user.str.contains(r"\$")]
    
#     # Keep failed logins
#     failures = df[df.result == "Fail"]
    
#     # Keep cross-host authentication
#     cross_host = df[df.src_pc != df.dst_pc]
    
#     # Keep only interesting logon types
#     # interesting_types = df[df.logon_type.isin([2, 3, 10])]
#     interesting_types = df[df.logon_type.isin(['Interactive', 'Network', 'RemoteInteractive'])]
    
#     return pd.concat([failures, cross_host, interesting_types]).drop_duplicates()

# # filter for only suspicious processes
# def filter_process(df):
#     # v1
#     # # Keep only processes that are not common
#     # common_processes = ["explorer.exe", "cmd.exe", "powershell.exe"]
#     # return df[~df.proc_name.isin(common_processes)]
#     SUSPICIOUS_PROCS = [
#     "powershell.exe", "cmd.exe", "wmic.exe",
#     "psexec.exe", "net.exe", "whoami.exe",
#     "rundll32.exe", "reg.exe", "sc.exe"
#     ]
#     # v2
#     df = df[df.proc_name.str.lower().isin(SUSPICIOUS_PROCS)]
#     return df

def normalize_auth(row):
    # og description: f"{row.result} login attempt for {row.src_user} from {row.src_host} to {row.dst_host} using {row.auth_type}"
    return {
        "timestamp": row.timestamp,
        "host": row.dst_host,
        "user": row.src_user,
        "event_type": "authentication",
        "description": f"{row.result} login attempt for user \'{row.src_user}\' from host {row.src_host} to host {row.dst_host} using {row.auth_type} logon type"
    }

def normalize_proc(row):
   # original description: f"Process {row.proc_name} executed by {row.user} on {row.host} with command: {row.command}"
   # og desc 2: f"Process {row.process} executed by {row.user} on {row.host} with action: {row.action}"
    return {
        "timestamp": row.timestamp,
        "host": row.host,
        "user": row.user,
        "event_type": "process",
        "description": f"Process {row.proc_name} executed by user \'{row.user}\' on host {row.host} with action: {row.action}"
    }

def normalize_redteam(row):
    # og description: f"Red team activity: {row.user} moved from {row.src_host} to {row.dst_host}"
    return {
        "timestamp": row.timestamp,
        "host": row.dst_host,
        "user": row.user,
        "event_type": "redteam",
        "description": f"Red team activity: user \'{row.user}\' moved from host {row.src_host} to host {row.dst_host}"
    }

def main():
    # load data using functions from load_data.py 
    data_path = os.path.dirname(os.getcwd()) + "/data/"
    print(data_path)
    auth_df = load_auth(data_path + 'auth_part.txt')
    proc_df = load_process(data_path + 'proc_part.txt')
    auth_attack_df = load_auth(data_path + 'auth_attack.csv')
    proc_attack_df = load_process(data_path + 'proc_attack.csv')
    redteam_df = load_redteam(data_path + 'redteam.txt')


    # filter to only the top 1000 most recent entries for each dataset to make it more manageable for prompting and evaluation
    auth_df = filter_data(auth_df, 1000)
    proc_df = filter_data(proc_df, 1000)
    auth_attack_df = filter_data(auth_attack_df, 1000)
    proc_attack_df = filter_data(proc_attack_df, 1000)
    redteam_df = filter_data(redteam_df, 1000)
    
    # apply normalization functions to each dataset to create a consistent format for all events across datasets
    # auth_events = auth_df.apply(normalize_auth, axis=1)
    # proc_events = proc_df.apply(normalize_proc, axis=1)
    # auth_attack_events = auth_attack_df.apply(normalize_auth, axis=1)
    # proc_attack_events = proc_attack_df.apply(normalize_proc, axis=1)
    # redteam_events = redteam_df.apply(normalize_redteam, axis=1)

    # transform dictionaries into json format and output to cleaned_data folder as 'auth_cleaned.json', 'proc_cleaned.json', and 'redteam_cleaned.json' for use in the prompting and evaluation stages

    auth_json = auth_df.apply(normalize_auth, axis=1).tolist()
    proc_json = proc_df.apply(normalize_proc, axis=1).tolist()
    auth_attack_json = auth_attack_df.apply(normalize_auth, axis=1).tolist()
    proc_attack_json = proc_attack_df.apply(normalize_proc, axis=1).tolist()
    redteam_json = redteam_df.apply(normalize_redteam, axis=1).tolist()

    with open(os.path.dirname(os.getcwd()) + "/cleaned_data/auth_cleaned.json", "w") as f:
        json.dump(auth_json, f, indent=4)

    with open(os.path.dirname(os.getcwd()) + "/cleaned_data/proc_cleaned.json", "w") as f:
        json.dump(proc_json, f, indent=4)

    with open(os.path.dirname(os.getcwd()) + "/cleaned_data/auth_attack_cleaned.json", "w") as f:
        json.dump(auth_attack_json, f, indent=4)

    with open(os.path.dirname(os.getcwd()) + "/cleaned_data/proc_attack_cleaned.json", "w") as f:
        json.dump(proc_attack_json, f, indent=4)

    with open(os.path.dirname(os.getcwd()) + "/cleaned_data/redteam_cleaned.json", "w") as f:
        json.dump(redteam_json, f, indent=4)

if __name__ == "__main__":
    main()