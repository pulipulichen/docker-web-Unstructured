import hashlib
import json

def get_file_hash_key(chunk_config, file_path):
    
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    
    # Read the file in chunks to handle large files efficiently
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    
    if chunk_config is None:
        chunk_config = ''
    else:
        chunk_config = json.dumps(chunk_config)

    return 'unstrcutured_' + chunk_config + '_' + sha256_hash.hexdigest()