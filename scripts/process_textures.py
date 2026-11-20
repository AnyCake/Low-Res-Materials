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


def resize_keep_aspect(img: Image.Image, max_side: int) -> Image.Image:
    width, height = img.size
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid image dimensions: {width}x{height}")

    if width >= height:
        new_width = max_side
        new_height = max(1, round(height * (max_side / width)))
    else:
        new_height = max_side
        new_width = max(1, round(width * (max_side / height)))

    return img.resize((new_width, new_height), resample=Image.Resampling.NEAREST)


def process_image(src_path: Path) -> None:
    with Image.open(src_path) as raw:
        img = ImageOps.exif_transpose(raw).convert("RGB")

    stem = src_path.stem

    for size, out_dir in SIZES.items():
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{stem}.png"
        resized = resize_keep_aspect(img, size)
        resized.save(out_path, format="PNG", optimize=True)


def main() -> None:
    if not INPUT_DIR.exists():
        print("Directory 'Original-Photos' not found.")
        return

    files = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    )

    if not files:
        print("No images found to process.")
        return

    for file_path in files:
        process_image(file_path)
        print(f"Processed: {file_path.name}")


if __name__ == "__main__":
    main()
