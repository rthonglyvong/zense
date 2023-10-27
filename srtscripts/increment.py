import sys
import re
import os

def increment_srt_indexes(srt_file_path, increment_value):
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    def increment_index(match):
        index = int(match.group(1))
        new_index = index + increment_value
        return f"{new_index:0>2}\n"  # Add a newline after the incremented index

    pattern = re.compile(r"(\d+)\n")
    new_srt_content = pattern.sub(increment_index, srt_content)

    # Extract directory and file name
    file_dir, file_name = os.path.split(srt_file_path)
    incremented_file_path = os.path.join(file_dir, "incremented_" + file_name)

    with open(incremented_file_path, 'w', encoding='utf-8') as file:
        file.write(new_srt_content)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py path_to_srt increment_value")
        sys.exit(1)

    srt_file_path = sys.argv[1]
    try:
        increment_value = int(sys.argv[2])
    except ValueError:
        print("Please enter a valid integer for the increment value.")
        sys.exit(1)

    increment_srt_indexes(srt_file_path, increment_value)
    print(f"Incremented SRT file saved as 'incremented_{srt_file_path}'")

if __name__ == "__main__":
    main()
