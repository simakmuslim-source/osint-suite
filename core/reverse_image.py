"""
Reverse image search using perceptual hashing (imagehash)
Can later be extended with image-match Elasticsearch backend.
"""

from pathlib import Path
from typing import List, Tuple
from PIL import Image
import imagehash

def phash_search(query_path: str, database_folder: str, threshold: int = 10) -> List[Tuple[str, int]]:
    """
    Find similar images in a local folder using perceptual hash.
    Returns list of (path, distance) sorted by distance.
    """
    query_hash = imagehash.phash(Image.open(query_path))
    matches = []

    for img_path in Path(database_folder).rglob("*.*"):
        if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            continue
        try:
            h = imagehash.phash(Image.open(img_path))
            dist = query_hash - h
            if dist <= threshold:
                matches.append((str(img_path), int(dist)))
        except Exception:
            continue

    return sorted(matches, key=lambda x: x[1])
