import time


def read_file_to_array(filename):
    text_array = []
    with open(filename, "rt") as f:
        line = f.readline()
        while line:
            text_array.append(line)
            line = f.readline()
    return text_array

def write_array_to_file(filename, text_array):
    with open(filename, "wt") as f:
        for text in text_array:
            f.write(text)

def log_message(filename, error):
    (y, m, d, h, m, s, _, _) = time.localtime()
    moment = f"{y}/{m}/{d} {h}:{m}:{s}"
    
    text_array = read_file_to_array(filename)
    text_array.append(f"[{moment}]: {error}\n")
    write_array_to_file(filename, text_array)