import pandas as pd

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

def filter_days(df, day_start, day_end):
    return df[(df.timestamp >= day_start) & (df.timestamp <= day_end)]

