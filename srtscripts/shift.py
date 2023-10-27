import sys
import re
from datetime import datetime, timedelta
import os

def shift_srt_time(original_time, seconds_to_shift):
    time_format = "%H:%M:%S,%f"
    datetime_obj = datetime.strptime(original_time, time_format)
    shifted_time = datetime_obj + timedelta(seconds=seconds_to_shift)
    return shifted_time.strftime(time_format)[:-3]  # omitting last 3 digits to keep 3 decimal precision

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py path_to_srt seconds_to_shift")
        sys.exit(1)

    srt_file_path = sys.argv[1]
    try:
        seconds_to_shift = float(sys.argv[2])
    except ValueError:
        print("Please enter a valid number for seconds to shift")
        sys.exit(1)

    if not os.path.isfile(srt_file_path):
        print(f"The file '{srt_file_path}' does not exist.")
        sys.exit(1)

    # Extract directory and file name
    file_dir, file_name = os.path.split(srt_file_path)
    
    with open(srt_file_path, 'r', encoding="utf-8") as file:
        srt_content = file.read()

    pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
    
    def replace_time(match):
        start_time = match.group(1)
        end_time = match.group(2)
        new_start_time = shift_srt_time(start_time, seconds_to_shift)
        new_end_time = shift_srt_time(end_time, seconds_to_shift)
        return f"{new_start_time} --> {new_end_time}"

    new_srt_content = pattern.sub(replace_time, srt_content)

    shifted_file_path = os.path.join(file_dir, "shifted_" + file_name)

    with open(shifted_file_path, 'w', encoding="utf-8") as file:
        file.write(new_srt_content)

    print(f"Shifted .srt file saved as '{shifted_file_path}'")

if __name__ == "__main__":
    main()
