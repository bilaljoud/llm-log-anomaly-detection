import random

import pandas as pd
import json
from clean_data import normalize_auth, normalize_proc, normalize_redteam
import os

# def aggregate_data(auth_df, proc_df, redteam_df):
#     # Normalize and combine datasets
#     auth_events = auth_df.apply(normalize_auth, axis=1)
#     proc_events = proc_df.apply(normalize_proc, axis=1)
#     redteam_events = redteam_df.apply(normalize_redteam, axis=1)
    
#     # Combine all events into a single DataFrame
#     combined_df = pd.DataFrame(list(auth_events) + list(proc_events) + list(redteam_events))
    
#     # Sort by timestamp
#     combined_df.sort_values(by="timestamp", inplace=True)
    
#     return combined_df

def correlate_redteam_events(redteam_df, auth_df, proc_df):
    # ideally, want to correlate on timestamp to get events from auth and proc that match the same timestamp as red team activity to get meaningful sequences
    pass

# def create_prompt_sequences(, type):

# This function will load the cleaned and normalized datasets for auth and proc both attack and standard and put them into distinct data streams and log sequences of anomalous and non-anomalous events to be used for prompting and evaluation
def aggregate_data():
    cleaned_data_path = os.path.dirname(os.getcwd()) + "/cleaned_data/"
    print(cleaned_data_path)
    
    # load cleaned datasets
    auth_json = pd.read_json(cleaned_data_path + 'auth_cleaned.json')
    proc_json = pd.read_json(cleaned_data_path + 'proc_cleaned.json')
    auth_attack_json = pd.read_json(cleaned_data_path + 'auth_attack_cleaned.json')
    proc_attack_json = pd.read_json(cleaned_data_path + 'proc_attack_cleaned.json')
    redteam_json = pd.read_json(cleaned_data_path + 'redteam_cleaned.json')

    # choose baseline data for few-shot prompting and differentiating anomalous and non-anomalous events for evaluation
    train_baseline_auth_json = auth_json.sample(n=10) 
    train_anomalous_auth_json = auth_attack_json.sample(n=10) 

    train_baseline_proc_json = proc_json.sample(n=10)
    train_anomalous_proc_json = proc_attack_json.sample(n=10) 

    train_baseline_auth_sequence = train_baseline_auth_json.apply(lambda row: f"{row.description}", axis=1).tolist()
    train_baseline_proc_sequence = train_baseline_proc_json.apply(lambda row: f"{row.description}", axis=1).tolist()
    train_anomalous_auth_sequence = train_anomalous_auth_json.apply(lambda row: f"{row.description}", axis=1).tolist()
    train_anomalous_proc_sequence = train_anomalous_proc_json.apply(lambda row: f"{row.description}", axis=1).tolist()
    
    baseline_sequence = random.sample(train_baseline_auth_sequence + train_baseline_proc_sequence, k=20)
    anomalous_sequence = random.sample(train_anomalous_auth_sequence + train_anomalous_proc_sequence, k=20)

    few_shot_prompting_data = {
        "baseline_sequence": baseline_sequence,
        "anomalous_sequence": anomalous_sequence
    }

    with open(os.path.dirname(os.getcwd()) + "/prompting_data/few_shot_prompting_data.json", "w") as f:
        json.dump(few_shot_prompting_data, f, indent=4)

    # datasets should contain 20 logs in each sequence, with a total of 100 sequences for each of the 3 categories (anomalous, normal, mixed) for a total of 300 sequences to be used for prompting and evaluation
    eval_dataset = []
    log_seq_num = 0
    # create dataset with purely anomalous auth and proc logs, tag it as "anomalous" for evaluation purposes
    # format:
    # {
    #   "tag": "anomalous",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }
    # want to split it by sequential timestamp
    # anomalous_auth_sequence = anomalous_auth_json.sort_values(by="timestamp").apply(lambda row: f"Anomalous auth event: {row.description}", axis=1).tolist()
    # for now just randomly sample 20 logs from the anomalous auth and proc datasets to create anomalous sequences for evaluation, will implement sequential splitting by timestamp in future iterations
    for i in range(35):
        log_seq_num += 1
        anomalous_auth_sequence = auth_attack_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        anomalous_proc_sequence = proc_attack_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        anomalous_sequence = random.sample(anomalous_auth_sequence + anomalous_proc_sequence, k=20)
        anomalous_data_point = {
            "sequence_id": log_seq_num,
            "tag": "anomalous",
            "log_seq": anomalous_sequence
        }
        eval_dataset.append(anomalous_data_point)


    # create dataset with purely non-anomalous auth and proc logs, tag it as "normal" for evaluation purposes
    # format:
    # {
    #   "tag": "normal",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }
    # want to split by sequentioal timestamp to get realistic sequences of auth and proc activity
    # normalize_auth(proc_json.iloc[0])
    for i in range(100):
        log_seq_num += 1
        normal_auth_sequence = auth_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        normal_proc_sequence = proc_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        normal_sequence = random.sample(normal_auth_sequence + normal_proc_sequence, k=20)
        normal_data_point = {
            "sequence_id": log_seq_num,
            "tag": "normal",
            "log_seq": normal_sequence
        }
        eval_dataset.append(normal_data_point)

    # create mixed dataset with both anomalous and non-anomalous auth and proc logs, tag it as "mixed" for evaluation purposes (trending towards anomalous to make it more challenging for the model)
    # format:
    # {
    #   "tag": "mixed",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }
    for i in range(15):
        log_seq_num += 1
        mixed_auth_sequence = auth_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist() + auth_attack_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        mixed_proc_sequence = proc_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist() + proc_attack_json.sample(n=10).apply(lambda row: f"{row.description}", axis=1).tolist()
        mixed_sequence = random.sample(mixed_auth_sequence + mixed_proc_sequence, k=20)
        mixed_data_point = {
            "sequence_id": log_seq_num,
            "tag": "mixed",
            "log_seq": mixed_sequence
        }
        eval_dataset.append(mixed_data_point)


    # create dataset with red team activity logs, tag it as "redteam" for evaluation purposes
    # later

    # shuffle the eval dataset to ensure random distribution of anomalous, normal, and mixed sequences for prompting and evaluation
    random.shuffle(eval_dataset) 

    # re-tagging the sequence-ids after shuffling
    for i in range(0, len(eval_dataset)):
        eval_dataset[i]["sequence_id"] = i + 1

    # output log sequences along with their associated labels (anomalous, normal, mixed, redteam) in another json file called 'prompting_data.json' to be used for prompting and evaluation

    with open(os.path.dirname(os.getcwd()) + "/prompting_data/eval_dataset.json", "w") as f:
        json.dump(eval_dataset, f, indent=4)

    # eval dataset WAS 300 data points with 100 normal, 100 anomalous, and 100 mixed and each sequence had 40 logs, changed it
    # eval dataset should not have 150 data points (log sequences); first 100 are normal, 35 are anomalous, 15 are mixed; each log sequence should contain 20 logs (10 auth and 10 proc) to be used for prompting and evaluation
    # this should in theory be sufficient for results

if __name__ == "__main__":
    aggregate_data()