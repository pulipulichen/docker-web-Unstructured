import hashlib

def get_file_hash_key(item_id, file_path):
    
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    
    # Read the file in chunks to handle large files efficiently
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    
    if item_id is None:
        item_id = ''

    return 'file_' + item_id + '_' + sha256_hash.hexdigest()