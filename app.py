"""Simple OCR/field extraction baseline with a built-in text demo."""
import argparse
import json
import re
from pathlib import Path

SAMPLE = "Invoice No: INV-2026-103\nDate: 2026-10-16\nTotal: 1250.50\n"

def extract(text):
    patterns = {
        "invoice_number": r"Invoice\s*No\s*:\s*([A-Z0-9-]+)",
        "date": r"Date\s*:\s*(\d{4}-\d{2}-\d{2})",
        "total": r"Total\s*:\s*([\d,.]+)",
    }
    fields = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        fields[name] = {"value": match.group(1) if match else None,
                        "needs_review": match is None}
    return fields

def image_text(path):
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Install optional packages: pip install pytesseract pillow") from exc
    return pytesseract.image_to_string(Image.open(path))  # needs local Tesseract engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path)
    parser.add_argument("--text-file", type=Path)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    text = image_text(args.image) if args.image else (args.text_file.read_text(encoding="utf-8") if args.text_file else SAMPLE)
    print(json.dumps({"fields": extract(text), "source": "demo" if not args.image and not args.text_file else "input"}, indent=2))
