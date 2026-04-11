import pandas as pd
import os

def load_auth(path):
    cols = [
        "timestamp","src_user","dst_user",
        "src_host","dst_host","auth_type","logon_type", "auth_orientation", "result"
    ]
    df = pd.read_csv(path, names=cols)
    return df

def load_process(path):
    cols = [
        "timestamp","user","host","proc_name","action"
    ]
    df = pd.read_csv(path, names=cols)
    return df

def load_redteam(path):
    cols = [
        "timestamp","user","src_host","dst_host"
    ]
    df = pd.read_csv(path, names=cols)
    return df

# def filter_days(df, day_start, day_end):
#     return df[(df.timestamp >= day_start) & (df.timestamp <= day_end)]
# def filter_days(df, day_start, day_end):
#     df['timestamp'] = pd.to_datetime(df['timestamp'])
#     return df[(df.timestamp >= day_start) & (df.timestamp <= day_end)]
def filter_data(df, num_entries):
    return df.head(num_entries)


# # Testing data loading
# def main():
#     data_path = os.path.dirname(os.getcwd()) + "/data/"
#     print(data_path)
#     auth_df = load_auth(data_path + 'auth_part.txt')
#     proc_df = load_process(data_path + 'proc_part.txt')
#     auth_attack_df = load_auth(data_path + 'auth_attack.csv')
#     proc_attack_df = load_process(data_path + 'proc_attack.csv')
#     redteam_df = load_redteam(data_path + 'redteam.txt')
    
#     # # Example of filtering by day
#     # auth_df = filter_days(auth_df, "2021-01-01", "2021-01-31")
#     # proc_df = filter_days(proc_df, "2021-01-01", "2021-01-31")
#     # redteam_df = filter_days(redteam_df, "2021-01-01", "2021-01-31")
    
#     print(auth_df.head())
#     print(proc_df.head())
#     print(redteam_df.head())
#     print(auth_attack_df.head())
#     print(proc_attack_df.head())

# if __name__ == "__main__":
#     main()