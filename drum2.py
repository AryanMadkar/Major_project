from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import sys

import requests


DEFAULT_ROOT = Path(__file__).resolve().parent / "dev-clean" / "LibriSpeech" / "dev-clean"
DEFAULT_ENDPOINT = "http://localhost:8010/verify"
VALID_AUDIO_EXTENSIONS = {".flac", ".wav", ".mp3", ".ogg", ".m4a"}


@dataclass(frozen=True)
class AudioPair:
    label: str
    speaker_a: str
    speaker_b: str
    audio1: Path
    audio2: Path


def iter_speaker_dirs(root: Path) -> list[Path]:
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name)


def list_audio_files(speaker_dir: Path) -> list[Path]:
    audio_files = [item for item in speaker_dir.rglob("*") if item.is_file() and item.suffix.lower() in VALID_AUDIO_EXTENSIONS]
    return sorted(audio_files)


def build_pairs(root: Path, max_people: int | None = None) -> list[AudioPair]:
    speakers: list[tuple[str, list[Path]]] = []

    for speaker_dir in iter_speaker_dirs(root):
        audio_files = list_audio_files(speaker_dir)
        if len(audio_files) >= 2:
            speakers.append((speaker_dir.name, audio_files))

    pairs: list[AudioPair] = []

    if max_people is not None:
        speakers = speakers[:max_people]

    for index in range(0, len(speakers), 3):
        chunk = speakers[index : index + 3]
        if len(chunk) < 2:
            break

        first_speaker, first_files = chunk[0]
        second_speaker, second_files = chunk[1]

        pairs.append(
            AudioPair(
                label="same",
                speaker_a=first_speaker,
                speaker_b=first_speaker,
                audio1=first_files[0],
                audio2=first_files[1],
            )
        )

        pairs.append(
            AudioPair(
                label="same",
                speaker_a=second_speaker,
                speaker_b=second_speaker,
                audio1=second_files[0],
                audio2=second_files[1],
            )
        )

        if len(chunk) == 3:
            third_speaker, third_files = chunk[2]
            pairs.append(
                AudioPair(
                    label="different",
                    speaker_a=first_speaker,
                    speaker_b=third_speaker,
                    audio1=first_files[0],
                    audio2=third_files[0],
                )
            )

    return pairs


def post_pair(endpoint: str, pair: AudioPair, timeout: float = 120.0) -> dict:
    with pair.audio1.open("rb") as audio1_file, pair.audio2.open("rb") as audio2_file:
        response = requests.post(
            endpoint,
            files={
                "audio1": (pair.audio1.name, audio1_file),
                "audio2": (pair.audio2.name, audio2_file),
            },
            timeout=timeout,
        )

    response.raise_for_status()
    payload = response.json()

    if isinstance(payload, dict) and payload.get("data") is not None:
        return payload["data"]

    return payload


def run(root: Path, endpoint: str, limit: int | None = None, people: int | None = None) -> None:
    if not root.exists():
        raise FileNotFoundError(f"Dataset root not found: {root}")

    pairs = build_pairs(root, max_people=people)
    if limit is not None:
        pairs = pairs[:limit]

    if not pairs:
        print("No usable speaker pairs found.")
        return

    correct = 0
    total = 0

    total_pairs = len(pairs)

    def render_progress(current: int) -> None:
        bar_width = 28
        ratio = current / total_pairs if total_pairs else 1.0
        filled = int(bar_width * ratio)
        bar = "#" * filled + "-" * (bar_width - filled)
        percent = ratio * 100
        sys.stdout.write(f"\r[{bar}] {current}/{total_pairs} ({percent:5.1f}%)")
        sys.stdout.flush()

    for index, pair in enumerate(pairs, start=1):
        result = post_pair(endpoint, pair)
        prediction = result.get("final_decision")
        expected = "same_speaker" if pair.label == "same" else "different_speaker"
        is_correct = prediction == expected
        correct += int(is_correct)
        total += 1
        render_progress(index)

    sys.stdout.write("\n")

    accuracy = correct / total if total else 0.0
    print(f"Summary: {correct}/{total} correct ({accuracy:.2%})")
    print(f"Endpoint: {endpoint}")
    print(f"Dataset root: {root}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run speaker-verification checks on LibriSpeech dev-clean.")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Path to the dev-clean dataset root.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Verification endpoint to call.")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on the number of pairs to test.")
    parser.add_argument("--people", type=int, default=None, help="Limit to the first N speakers (people) in the dataset.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.root, args.endpoint, args.limit, people=args.people)


if __name__ == "__main__":
    main()