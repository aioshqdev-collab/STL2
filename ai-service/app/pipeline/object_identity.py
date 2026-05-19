from pathlib import Path


def identify_object(image_path: Path) -> tuple[str, float]:
    """
    Placeholder for object recognition.

    Production options:
    - CLIP / SigLIP classifier for category hints.
    - Florence / BLIP-style captioner for natural-language prompts.
    - SAM 3 text/object segmentation when available.
    """
    stem = image_path.stem.replace("_", " ").replace("-", " ").strip()
    if stem:
        return stem[:60], 0.35
    return "unknown object", 0.0
