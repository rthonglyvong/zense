import keyboard
import time
import os
import sys

def clear_screen():
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(seconds):
    """Convert seconds to SRT time format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds*1000):03}"

def read_lyrics(file_path):
    """Read lyrics from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def read_romanized(file_path):
    """Read romanized text from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Input the start time and index
subfolder_path = sys.argv[1]
os.chdir(subfolder_path)
# Read the file content
with open('args.txt', 'r') as file:
    content = file.read().strip()
    print(content)

# Split the content by comma and strip any whitespace
values = [x.strip() for x in content.split(',')]

# Assuming the file always has two values, assign them to variables
initial_offset, start_index = float(values[0]), int(values[1])
# initial_offset = float(sys.argv[1])
# start_index = int(sys.argv[2])
# initial_offset = float(input("Enter the start time (in seconds): "))
# start_index = int(input("Enter the start index: "))

lyrics = read_lyrics('lyrics.txt')
romanized = read_romanized('romanized.txt')

# Ensure the lyrics and romanized files have the same line count
if len(lyrics) != len(romanized):
    raise ValueError("The lyrics and romanized files do not have the correct line counts.")

captions = []

first_space_pressed = False  # Flag to track the first spacebar press
current_time = initial_offset
reference_time = None

for i, lyric in enumerate(lyrics):
    if not lyric.strip():
        continue 
    clear_screen()
    
    # Display current and next romanized line
    print(f"Current line: {romanized[i]}")
    if i + 1 < len(romanized):
        print(f"Next line: {romanized[i+1]}")

    print("\nPress SPACE to START the caption.")
    keyboard.wait('space')

    if not first_space_pressed:
        reference_time = time.time()  # Initialize reference time on the first space press
        first_space_pressed = True

    caption_start_time = time.time() - reference_time + initial_offset

    clear_screen()
    print(f"Current line: {romanized[i]}")
    if i + 1 < len(romanized):
        print(f"Next line: {romanized[i+1]}")
    print("\nPress SPACE to END the caption.")
    keyboard.wait('space')
    caption_end_time = time.time() - reference_time + initial_offset

    captions.append(f"{start_index}\n")
    captions.append(f"{format_time(caption_start_time)} --> {format_time(caption_end_time)}\n")
    captions.append(f"{lyric}\n\n")
    start_index += 1

# Save to an SRT file with UTF-8 encoding
with open("output.srt", "w", encoding="utf-8") as file:
    file.writelines(captions)

clear_screen()
print("SRT file generated: output.srt")
