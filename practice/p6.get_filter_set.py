def get_filter_set(filter_dict, size):
    key = f"size_{size}"
    return filter_dict.get(key)
