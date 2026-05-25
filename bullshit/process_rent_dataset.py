#!/usr/bin/env python3
"""Process markdown files in multi_property_dataset/rent using the phase0 splitter.

Creates a `responses/` directory under the repo root and writes a JSON file
and a plain-text file for each input markdown containing the extracted
single-line property messages.

Usage:
    python process_rent_dataset.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_phase0_module(phase0_path: Path):
    spec = importlib.util.spec_from_file_location("phase0", str(phase0_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    repo_root = Path(__file__).resolve().parent

    phase0_path = repo_root / "extractor" / "phase0.py"
    if not phase0_path.exists():
        print("Cannot find phase0.py at", phase0_path)
        sys.exit(1)

    phase0 = load_phase0_module(phase0_path)

    # prefer the compatibility wrapper, fall back to improved
    splitter = getattr(phase0, "split_property_messages", None) or getattr(phase0, "split_property_messages_improved")
    if not callable(splitter):
        print("No splitter function found in phase0.py")
        sys.exit(1)

    # read from the 'requirement' folder as requested
    dataset_dir = repo_root / "multi_property_dataset" / "requirement"
    if not dataset_dir.exists():
        print("Dataset directory not found:", dataset_dir)
        sys.exit(1)

    out_dir = repo_root / "responses_requirements"
    out_dir.mkdir(exist_ok=True)

    md_files = sorted(dataset_dir.glob("*.md"))
    if not md_files:
        print("No .md files found in", dataset_dir)
        return

    for md in md_files:
        print("Processing", md.name)
        text = md.read_text(encoding="utf-8")

        try:
            messages = splitter(text)
        except TypeError:
            # some splitter versions expect different args
            messages = splitter(text, use_llm=False)
        except Exception as e:
            print(f"Error processing {md.name}: {e}")
            messages = []

        out_json = out_dir / f"{md.stem}.responses.json"
        out_txt = out_dir / f"{md.stem}.responses.txt"

        out_json.write_text(json.dumps({"source": str(md), "messages": messages}, indent=2, ensure_ascii=False), encoding="utf-8")
        out_txt.write_text("\n\n".join(messages), encoding="utf-8")

    print("Done. Responses saved to:", out_dir)


if __name__ == "__main__":
    main()
