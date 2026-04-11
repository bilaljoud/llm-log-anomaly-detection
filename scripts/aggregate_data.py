import pandas as pd
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

# This function will load the cleaned and normalized datasets for auth and proc both attack and standard and put them into distinct data streams and log sequences of anomalous and non-anomalous events to be used for prompting and evaluation
def aggregate_data():
    data_path = os.path.dirname(os.getcwd()) + "/cleaned_data/"
    print(data_path)
    
    # load cleaned datasets
    auth_json = pd.read_json(data_path + 'auth_cleaned.json')
    proc_json = pd.read_json(data_path + 'proc_cleaned.json')
    auth_attack_json = pd.read_json(data_path + 'auth_attack_cleaned.json')
    proc_attack_json = pd.read_json(data_path + 'proc_attack_cleaned.json')
    redteam_json = pd.read_json(data_path + 'redteam_cleaned.json')
    
    # datasets should contain 10 logs in each sequence, with a total of 100 sequences for each of the 4 categories (anomalous, normal, mixed, redteam) for a total of 400 sequences to be used for prompting and evaluation

    # create dataset with purely anomalous auth and proc logs, tag it as "anomalous" for evaluation purposes
    # format:
    # {
    #   "tag": "anomalous",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }


    # create dataset with purely non-anomalous auth and proc logs, tag it as "normal" for evaluation purposes
    # format:
    # {
    #   "tag": "normal",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }


    # create mixed dataset with both anomalous and non-anomalous auth and proc logs, tag it as "mixed" for evaluation purposes (trending towards anomalous to make it more challenging for the model)
    # format:
    # {
    #   "tag": "mixed",
    #   "log_seq": [
    #       log_description_1,
    #       log_description_2,
    #   ]
    # }



    # create dataset with red team activity logs, tag it as "redteam" for evaluation purposes


    # output log sequences along with their associated labels (anomalous, normal, mixed, redteam) in another json file called 'prompting_data.json' to be used for prompting and evaluation


    pass

if __name__ == "__main__":
    aggregate_data()