LABEL_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X",
    "X": "X"
}

def normalize_label(raw_label):
    
    return LABEL_MAP[raw_label.lower()].get()
