# app/utils/filename.py
import re

def normalize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()
