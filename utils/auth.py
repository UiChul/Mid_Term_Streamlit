import hashlib

def hash_pattern(pattern_list):
    
    pattern_str = "".join(map(str, pattern_list))
    return hashlib.sha256(pattern_str.encode()).hexdigest()