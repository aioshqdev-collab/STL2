from pathlib import Path


def reconstruct_mesh(segmented_image: Path, output_dir: Path, provider: str, quality: str) -> dict[str, Path]:
    """
    Single-image 3D reconstruction adapter.

    Replace the mock branch with one of:
    - Stable Fast 3D: best first target for textured GLB/OBJ.
    - TripoSR: simpler local fallback.
    - InstantMesh: slower but often stronger geometry.
    - SAM 3D Objects: object-aware long-term target.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    if provider == "mock":
        return write_mock_outputs(output_dir)

    raise NotImplementedError(
        f"Provider `{provider}` is not wired yet. Add the model call in app/pipeline/reconstruction.py."
    )


def write_mock_outputs(output_dir: Path) -> dict[str, Path]:
    glb = output_dir / "model.glb"
    obj = output_dir / "model.obj"
    stl = output_dir / "model.stl"
    texture = output_dir / "texture.png"

    glb.write_bytes(b"")
    texture.write_bytes(b"")
    obj.write_text(
        "\n".join(
            [
                "o placeholder",
                "v -10 -10 0",
                "v 10 -10 0",
                "v 0 10 0",
                "f 1 2 3",
                "",
            ]
        ),
        encoding="utf-8",
    )
    stl.write_text(
        "\n".join(
            [
                "solid placeholder",
                " facet normal 0 0 1",
                "  outer loop",
                "   vertex -10 -10 0",
                "   vertex 10 -10 0",
                "   vertex 0 10 0",
                "  endloop",
                " endfacet",
                "endsolid placeholder",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"glb": glb, "obj": obj, "stl": stl, "texture": texture}
