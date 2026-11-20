from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "Original-Photos"
SIZES = {
    64: ROOT / "64p",
    128: ROOT / "128p",
    256: ROOT / "256p",
}
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def clear_output_dirs() -> None:
    for out_dir in SIZES.values():
        out_dir.mkdir(parents=True, exist_ok=True)
        for item in out_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()


def process_image(src_path: Path) -> None:
    with Image.open(src_path) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")

    stem = src_path.stem

    for size, out_dir in SIZES.items():
        out_path = out_dir / f"{stem}.png"
        square = ImageOps.fit(
            img,
            (size, size),
            method=Image.Resampling.NEAREST,
            centering=(0.5, 0.5),
        )
        square.save(out_path, format="PNG", optimize=True)


def main() -> None:
    clear_output_dirs()

    if not INPUT_DIR.exists():
        print("Directory 'Original-Photos' not found. Cleared output directories.")
        return

    files = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    )

    if not files:
        print("No images found to process. Cleared output directories.")
        return

    for file_path in files:
        process_image(file_path)
        print(f"Processed: {file_path.name}")


if __name__ == "__main__":
    main()
