from pathlib import Path
from shutil import copyfile


def remove_background(image_path: Path, output_dir: Path) -> Path:
    """
    Placeholder background removal.

    Install `rembg` or SAM/SAM 3 segmentation in production and return a
    transparent PNG focused on the main object.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "segmented.png"
    copyfile(image_path, output_path)
    return output_path
