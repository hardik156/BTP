import os
import pyshark
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import time
from collections import defaultdict

def extract_features_from_pcap(file_path):

    original_features = []
    reverse_features = []
    start_time = time.time()
    bssid = "d8:44:89:f4:6f:0e"
    hostmac = "c0:1c:30:38:dc:4b"
    try:

        pair_packet_count = defaultdict(int)
        pair_interarrival_times = defaultdict(list)
        pair_packet_sizes = defaultdict(list)

        last_timestamps = {}


        capture = pyshark.FileCapture(file_path, display_filter=f"wlan.bssid == {bssid} && wlan.ra == {hostmac}")
        
        for packet in capture:
            try:
                pair = (1,2)

                pair_packet_count[pair] += 1

                current_time = float(packet.sniff_timestamp)
                if pair in last_timestamps:
                    interarrival_time = current_time - last_timestamps[pair]
                    pair_interarrival_times[pair].append(interarrival_time)
                last_timestamps[pair] = current_time

                if hasattr(packet, 'length'):
                    pair_packet_sizes[pair].append(int(packet.length))
            except AttributeError:
                continue
        
        capture.close()


        capture = pyshark.FileCapture(file_path, display_filter=f"wlan.bssid == {bssid} && wlan.ta == {hostmac}")
        
        for packet in capture:
            try:
                pair = (2,1)

                pair_packet_count[pair] += 1

                current_time = float(packet.sniff_timestamp)
                if pair in last_timestamps:
                    interarrival_time = current_time - last_timestamps[pair]
                    pair_interarrival_times[pair].append(interarrival_time)
                last_timestamps[pair] = current_time

                if hasattr(packet, 'length'):
                    pair_packet_sizes[pair].append(int(packet.length))
            except AttributeError:
                continue
        
        capture.close()

        most_frequent_pair = (1,2)
        reverse_pair = (most_frequent_pair[1], most_frequent_pair[0])
        interarrival_times = pair_interarrival_times[most_frequent_pair]
        packet_sizes = pair_packet_sizes[most_frequent_pair]

        avg_inter_arrival_time = np.mean(interarrival_times) if interarrival_times else 0
        
        std_inter_arrival_time = np.std(interarrival_times) if interarrival_times else 0
        
        avg_packet_size = np.mean(packet_sizes) if packet_sizes else 0
        avg_packets_per_second = len(interarrival_times) / (sum(interarrival_times) if interarrival_times else 1)

        original_features = [avg_inter_arrival_time, std_inter_arrival_time, avg_packet_size, avg_packets_per_second]

        interarrival_times = pair_interarrival_times[reverse_pair]
        packet_sizes = pair_packet_sizes[reverse_pair]

        avg_inter_arrival_time = np.mean(interarrival_times) if interarrival_times else 0
        std_inter_arrival_time = np.std(interarrival_times) if interarrival_times else 0
        avg_packet_size = np.mean(packet_sizes) if packet_sizes else 0
        avg_packets_per_second = len(interarrival_times) / (sum(interarrival_times) if interarrival_times else 1)

        reverse_features = [avg_inter_arrival_time, std_inter_arrival_time, avg_packet_size, avg_packets_per_second]
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    print(time.time() - start_time)
    print(original_features + reverse_features)
    return original_features + reverse_features



def write_features_to_txt(features, labels, output_file):
    with open(output_file, 'a') as f:
        for feature, label in zip(features, labels):
            feature_str = ', '.join(map(str, feature))  
            line = f"{feature_str}, {label}\n"  
            f.write(line)


def process_and_save_features(root_folder_path, output_txt_file):
    all_features = []
    all_labels = []
    

    folder_path = root_folder_path
    i = 0
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.pcapng'):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing file: {filename}")
                extracted_features = extract_features_from_pcap(file_path)
                if extracted_features:
                    if(i%3==0):
                        label = 0
                    elif(i%3==1):
                        label = 2
                    else:
                        label = 1
                    i+=1
                    print(label)
                    all_features.append(extracted_features)
                    all_labels.append(label)
                    write_features_to_txt([extracted_features], [label], output_txt_file)

    return all_features, all_labels



root_folder_path = "./filtered_packets"
output_txt_file = 'kismet-features.txt'

all_features, all_labels = process_and_save_features(root_folder_path, output_txt_file)

