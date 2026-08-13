LABEL_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X" 
}

def normalize_label(raw_label):
    
    return LABEL_MAP.get(raw_label.lower())
