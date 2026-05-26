import argparse
import json
import pathlib
import re
import urllib.request
from datetime import datetime
from typing import Any


EXCLUDE_KEYS = {"message_title", "metadata_summary", "railway_line", "extraction_meta"}


def norm(text: str) -> str:
    text = text.lower()
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def digits_only(text: str) -> str:
    return re.sub(r"\D", "", text)


def field_supported(field: str, value: Any, raw: str, nraw: str) -> bool:
    if value is None:
        return True

    if isinstance(value, bool):
        return True

    if field == "request_type":
        v = str(value).lower()
        if v == "rent":
            return any(k in nraw for k in [" rent ", "on rent", "for rent"]) or "rent" in nraw
        if v == "sale":
            return any(k in nraw for k in ["sale", "asking", "cr", "crore", "out rate", "outright"])
        if v == "requirement":
            return any(k in nraw for k in ["required", "requirement", "need", "looking for"])
        return str(value).lower() in nraw

    if field == "bhk":
        v = str(value)
        return any(p in nraw for p in [f"{v} bhk", f"{v}bhk", f"{v} rk", f"{v}rk"])

    if field in {"price", "price_min", "price_max", "rent_price", "deposit_price"}:
        if not isinstance(value, (int, float)):
            return False
        iv = int(value)
        if iv < 1000:
            return False
        return str(iv) in digits_only(raw)

    if field == "property_subtype":
        v = norm(str(value))
        aliases = {
            "apartment": ["apartment", "flat"],
            "flat": ["flat", "apartment"],
            "builder floor": ["builder floor"],
        }
        for alias in aliases.get(v, [v]):
            if alias in nraw:
                return True
        return False

    if field == "furnishing":
        v = norm(str(value))
        aliases = {
            "semi furnished": ["semi furnished", "semi furnish"],
            "fully furnished": ["fully furnished", "full furnished"],
            "unfurnished": ["unfurnished", "not furnished"],
        }
        return any(alias in nraw for alias in aliases.get(v, [v]))

    if isinstance(value, (int, float)):
        return str(int(value)) in digits_only(raw)

    if isinstance(value, str):
        v = norm(value)
        if not v:
            return True
        return v in nraw

    return True


def walk(prefix: str, obj: Any):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in EXCLUDE_KEYS:
                continue
            next_prefix = f"{prefix}.{key}" if prefix else key
            yield from walk(next_prefix, value)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                yield from walk(prefix, item)
            else:
                yield prefix, item
    else:
        yield prefix, obj


def run_all(dataset_dir: pathlib.Path, endpoint: str, output_path: pathlib.Path) -> None:
    files = sorted(dataset_dir.rglob("*.md"))

    global_total = 0
    global_supported = 0
    rows = []

    for file_path in files:
        raw = file_path.read_text(encoding="utf-8", errors="ignore")
        payload = json.dumps({"messages": [raw]}).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                parsed = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            rows.append(
                {
                    "path": str(file_path).replace("\\", "/"),
                    "raw": raw,
                    "response": {"error": str(exc)},
                    "supported": 0,
                    "total": 0,
                    "acc": 0.0,
                }
            )
            continue

        nraw = " " + norm(raw) + " "
        total = 0
        supported = 0
        for path_key, value in walk("", parsed):
            key = path_key.split(".")[-1]
            if value is None or key in EXCLUDE_KEYS:
                continue
            total += 1
            if field_supported(key, value, raw, nraw):
                supported += 1

        acc = (supported / total * 100) if total else 0.0
        global_total += total
        global_supported += supported

        rows.append(
            {
                "path": str(file_path).replace("\\", "/"),
                "raw": raw,
                "response": parsed,
                "supported": supported,
                "total": total,
                "acc": acc,
            }
        )

    overall_acc = (global_supported / global_total * 100) if global_total else 0.0

    parts = []
    parts.append("# Model Evaluation Report (All Single-Property Messages)")
    parts.append("")
    parts.append(f"- Generated: {datetime.now().isoformat(timespec='seconds')}")
    parts.append(f"- Endpoint: {endpoint}")
    parts.append(f"- Total messages: {len(files)}")
    parts.append(f"- Overall supported fields: {global_supported}/{global_total}")
    parts.append(f"- Overall accuracy: {overall_acc:.2f}%")
    parts.append("")

    for index, row in enumerate(rows, 1):
        parts.append(f"## {index}. {row['path']}")
        parts.append("")
        parts.append(f"- Sample accuracy: {row['acc']:.2f}% ({row['supported']}/{row['total']})")
        parts.append("")
        parts.append("### Original message")
        parts.append("")
        parts.append("```text")
        parts.append(row["raw"].rstrip("\n"))
        parts.append("```")
        parts.append("")
        parts.append("### Model response")
        parts.append("")
        parts.append("```json")
        parts.append(json.dumps(row["response"], ensure_ascii=False, indent=2))
        parts.append("```")
        parts.append("")

    output_path.write_text("\n".join(parts), encoding="utf-8")

    print(f"FILES={len(files)}")
    print(f"ACCURACY={overall_acc:.2f}")
    print(f"REPORT={output_path.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="single_property_Dataset")
    parser.add_argument("--url", default="http://127.0.0.1:8000/extract")
    parser.add_argument("--out", default="responsev2.md")
    args = parser.parse_args()

    run_all(pathlib.Path(args.dataset), args.url, pathlib.Path(args.out))


if __name__ == "__main__":
    main()
