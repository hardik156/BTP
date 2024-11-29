import os
import subprocess
from datetime import datetime
def get_capture_times(file_path):

    capinfos_command = ["capinfos", "-a", file_path]
    start_time = None
    try:
        result = subprocess.run(capinfos_command, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "First packet time:" in line:
                start_time = line.split("First packet time:")[1].strip()
                break
    except subprocess.CalledProcessError as e:
        print(f"Error running capinfos: {e}")

    tshark_command = [
        "tshark",
        "-r", file_path,
        "-T", "fields",
        "-e", "frame.time",
    ]
    last_time = None
    try:
        result = subprocess.run(tshark_command, capture_output=True, text=True, check=True)
        timestamps = result.stdout.strip().splitlines()
        if timestamps:
            raw_last_time = timestamps[-1]
            raw_last_time = raw_last_time.split(" India Standard Time")[0].strip()
            raw_last_time = raw_last_time[:raw_last_time.find(".") + 7]  
            last_time_obj = datetime.strptime(raw_last_time, "%b %d, %Y %H:%M:%S.%f")
            last_time = last_time_obj.strftime("%Y-%m-%d %H:%M:%S")
    except subprocess.CalledProcessError as e:
        print(f"Error running tshark: {e}")

    if start_time and last_time:
        print(f"File: {file_path}\nStart Time: {start_time}, End Time: {last_time}")
    else:
        print(f"Could not extract timestamps for {file_path}")
    return start_time, last_time

def slice_pcap_with_editcap(large_pcap, start_time, end_time, output_file):
    print(start_time,end_time)
    command = [
        "editcap",
        "-A", start_time,  
        "-B", end_time,    
        large_pcap,
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Filtered packets saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running editcap: {e}")

def process_folders(folders, large_pcap, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder in folders:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if file_path.endswith(".pcapng"):
                print(f"Processing file: {file_path}")
                start_time, end_time = get_capture_times(file_path)
                print(start_time,end_time)
                if start_time and end_time:
                    output_file = os.path.join(output_folder, f"{os.path.basename(file)}_filtered.pcapng")
                    slice_pcap_with_editcap(large_pcap, start_time, end_time, output_file)

folders = ["further_test_youtube", "further_test_netflix", "further_test_hotstar"] 
large_pcap = "../Kismet_capture/Kismet-20241112-12-12-30-1.pcapng" 
output_folder = "filtered_packets"  
process_folders(folders, large_pcap, output_folder)
