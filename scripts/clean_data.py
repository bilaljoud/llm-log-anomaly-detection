import pandas as pd

def filter_auth(df):
    # Remove machine accounts
    df = df[~df.src_user.str.contains(r"\$")]
    
    # Keep failed logins
    failures = df[df.result == "Fail"]
    
    # Keep cross-host authentication
    cross_host = df[df.src_pc != df.dst_pc]
    
    # Keep only interesting logon types
    interesting_types = df[df.logon_type.isin([2, 3, 10])]
    
    return pd.concat([failures, cross_host, interesting_types]).drop_duplicates()

# filter for only suspicious processes
def filter_process(df):
    # v1
    # # Keep only processes that are not common
    # common_processes = ["explorer.exe", "cmd.exe", "powershell.exe"]
    # return df[~df.proc_name.isin(common_processes)]
    SUSPICIOUS_PROCS = [
    "powershell.exe", "cmd.exe", "wmic.exe",
    "psexec.exe", "net.exe", "whoami.exe",
    "rundll32.exe", "reg.exe", "sc.exe"
    ]
    # v2
    df = df[df.process.str.lower().isin(SUSPICIOUS_PROCS)]
    return df

def normalize_auth(row):
    return {
        "timestamp": row.timestamp,
        "host": row.dst_host,
        "user": row.src_user,
        "event_type": "authentication",
        "description": f"{row.result} login attempt for {row.src_user} from {row.src_host} to {row.dst_host} using {row.auth_type}"
    }

def normalize_proc(row):
   # original description: f"Process {row.proc_name} executed by {row.user} on {row.host} with command: {row.command}"
    return {
        "timestamp": row.timestamp,
        "host": row.host,
        "user": row.user,
        "event_type": "process",
        "description": f"Process {row.process} executed by {row.user} on {row.host} with action: {row.action}"
    }