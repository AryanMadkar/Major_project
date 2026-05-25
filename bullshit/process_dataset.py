#!/usr/bin/env python3
"""Generic dataset processor for multi_property_dataset.

Usage examples:
  # process requirement -> responses_requirements
  python process_dataset.py --input multi_property_dataset/requirement --out responses_requirements

  # process sale -> responses_sales
  python process_dataset.py --input multi_property_dataset/sale --out responses_sales
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def load_phase0_module(phase0_path: Path):
    spec = importlib.util.spec_from_file_location("phase0", str(phase0_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def process_folder(phase0, input_dir: Path, out_dir: Path, overwrite: bool = True):
    splitter = getattr(phase0, "split_property_messages", None) or getattr(phase0, "split_property_messages_improved")
    if not callable(splitter):
        raise RuntimeError("No splitter function found in phase0.py")

    out_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(input_dir.glob("*.md"))
    if not md_files:
        print("No .md files found in", input_dir)
        return

    for md in md_files:
        print("Processing", md.name)
        text = md.read_text(encoding="utf-8")

        try:
            messages = splitter(text)
        except TypeError:
            messages = splitter(text, use_llm=False)
        except Exception as e:
            print(f"Error processing {md.name}: {e}")
            messages = []

        out_json = out_dir / f"{md.stem}.responses.json"
        out_txt = out_dir / f"{md.stem}.responses.txt"

        if not overwrite and out_json.exists():
            print("Skipping existing:", out_json.name)
            continue

        out_json.write_text(json.dumps({"source": str(md), "messages": messages}, indent=2, ensure_ascii=False), encoding="utf-8")
        out_txt.write_text("\n\n".join(messages), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Process multi-property markdown files into structured responses.")
    parser.add_argument("--input", "-i", type=str, default="multi_property_dataset/requirement", help="Input folder (relative to repo root)")
    parser.add_argument("--out", "-o", type=str, default="responses_requirements", help="Output folder (relative to repo root)")
    parser.add_argument("--no-overwrite", action="store_true", help="Do not overwrite existing outputs")

    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent
    phase0_path = repo_root / "extractor" / "phase0.py"
    if not phase0_path.exists():
        print("Cannot find phase0.py at", phase0_path)
        sys.exit(1)

    phase0 = load_phase0_module(phase0_path)

    input_dir = (repo_root / args.input).resolve()
    out_dir = (repo_root / args.out).resolve()

    if not input_dir.exists():
        print("Input folder does not exist:", input_dir)
        sys.exit(1)

    process_folder(phase0, input_dir, out_dir, overwrite=not args.no_overwrite)


if __name__ == "__main__":
    main()
