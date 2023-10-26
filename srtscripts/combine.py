import os
import re
from operator import itemgetter

def extract_srt_info(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        srt_content = srt_file.read()

    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n', re.DOTALL)
    srt_data = pattern.findall(srt_content)

    return [(int(index), start_time, end_time, caption) for index, start_time, end_time, caption in srt_data]

# Use os.path.dirname to get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(script_dir, "songs")

srt_info_list = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file == "output.srt":
            srt_path = os.path.join(root, file)
            srt_info = extract_srt_info(srt_path)
            srt_info_list.extend(srt_info)

srt_info_list.sort(key=itemgetter(0))

combined_srt_path = os.path.join(script_dir, "combined.srt")

with open(combined_srt_path, 'w', encoding='utf-8') as combined_srt_file:
    for index, start_time, end_time, caption in srt_info_list:
        combined_srt_file.write(f"{index}\n{start_time} --> {end_time}\n{caption}\n\n")
