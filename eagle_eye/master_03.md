# PHASE 2 — Video Metadata & Integrity Pipeline

Now the system becomes:

```text id="vgk8ul"
video-aware
```

This phase is extremely important because before doing ANY AI:

You must verify:

```text id="r4n2um"
"is this even a legitimate usable video?"
```

This layer protects your future AI pipeline from:

* corrupted videos
* replay attempts
* malformed uploads
* fake FPS tricks
* tiny resolution attacks
* frame injection
* weird codecs
* broken containers

---

# GOAL OF THIS PHASE

After upload:

```text id="l9owx9"
video.mp4
```

your server should analyze it and produce:

```json id="qfkt5f"
{
  "fps": 30,
  "duration": 5.2,
  "frame_count": 156,
  "resolution": "1280x720",
  "codec": "h264",
  "valid": true,
  "quality_score": 0.91
}
```

---

# WHY THIS PHASE MATTERS SO MUCH

Face AI models FAIL badly on:

* broken frames
* low FPS
* low resolution
* compressed videos
* unstable timing

You want:

```text id="m98mxu"
high-quality consistent input
```

before AI processing begins.

---

# WHAT WE WILL BUILD

# MODULES

| Module              | Purpose                   |
| ------------------- | ------------------------- |
| Video Reader        | open video safely         |
| Metadata Extractor  | extract properties        |
| Integrity Validator | detect corruption         |
| Quality Validator   | reject poor videos        |
| Security Validator  | detect suspicious uploads |
| Analysis Reporter   | structured results        |

---

# PROJECT STRUCTURE UPDATE

Add:

```text id="j5j4o2"
app/
│
├── services/
│   ├── video_metadata.py
│   ├── video_validator.py
│   ├── video_integrity.py
│   └── video_quality.py
```

---

# STEP 2.1 — Safe Video Opening

First:
learn to safely open videos.

---

# WHY SAFE OPENING MATTERS

Many videos:

* partially upload
* have broken containers
* fail decoding
* crash naive parsers

Your system should NEVER crash.

---

# WHAT TO VALIDATE

When opening:

| Check           | Purpose           |
| --------------- | ----------------- |
| can open        | corruption check  |
| readable frames | decode validation |
| has fps         | timing validity   |
| has dimensions  | usable video      |

---

# OUTPUT EXPECTATION

```json id="j0tyg7"
{
  "can_open": true,
  "readable": true
}
```

---

# STEP 2.2 — Extract Core Metadata

Now extract:

| Property    | Why Important               |
| ----------- | --------------------------- |
| FPS         | motion realism              |
| frame count | duration validation         |
| width       | quality                     |
| height      | quality                     |
| codec       | suspicious format detection |
| duration    | replay analysis             |

---

# IMPORTANT

DO NOT trust:

```text id="2x0yca"
duration metadata alone
```

Compute:

```text id="ycjlwm"
frame_count / fps
```

---

# WHY?

Metadata is sometimes fake or malformed.

---

# STEP 2.3 — FPS Validation

This is VERY important.

---

# WHY FPS MATTERS

Fake videos often:

* use 5 FPS
* duplicate frames
* generate unstable timing

Human movement analysis requires:

```text id="3wv3j9"
smooth temporal continuity
```

---

# RECOMMENDED RULES

| FPS   | Decision   |
| ----- | ---------- |
| < 15  | reject     |
| 15–24 | suspicious |
| 24–60 | ideal      |
| > 120 | suspicious |

---

# STEP 2.4 — Resolution Validation

Minimum:

```text id="6zxngv"
720p
```

Reject:

* tiny webcam faces
* pixelated attacks
* blurred replay videos

---

# RECOMMENDED MINIMUM

```python id="h4zivl"
1280x720
```

---

# WHY THIS MATTERS

Face embeddings become unstable when:

* eyes too small
* landmarks blurry
* skin texture missing

---

# STEP 2.5 — Duration Validation

Recommended:

```text id="c2q0ui"
3–15 seconds
```

---

# WHY?

Too short:

* insufficient movement
* weak liveness

Too long:

* storage waste
* attack surface increases

---

# STEP 2.6 — Frame Sampling Validation

Now verify:

```text id="rf8ojq"
frames can actually be decoded
```

---

# SAMPLE

Read:

* first frame
* middle frame
* last frame

---

# WHY?

Some corrupted videos:

* open successfully
* but fail later

VERY common.

---

# STEP 2.7 — Corruption Detection

Check for:

| Problem           | Detection        |
| ----------------- | ---------------- |
| unreadable frames | decode failures  |
| zero-byte frame   | corruption       |
| frozen frames     | replay suspicion |
| damaged stream    | codec issue      |

---

# IMPORTANT

DO NOT assume:

```text id="7e2krk"
successful upload == valid video
```

---

# STEP 2.8 — Frame Consistency Analysis

VERY important later for spoof detection.

Analyze:

* sudden frame jumps
* repeated frames
* abnormal timing

---

# WHY?

AI-generated/replayed videos often contain:

* repeated frames
* timing anomalies
* interpolation artifacts

---

# STEP 2.9 — Codec Validation

Whitelist codecs.

Allowed example:

* h264
* h265

Reject weird/uncommon codecs initially.

---

# WHY?

Exotic codecs:

* may fail inference pipeline
* may hide malformed streams
* complicate processing

---

# STEP 2.10 — Compression Artifact Analysis

This becomes important later.

For now:
store:

* bitrate
* compression ratio

---

# WHY?

Overcompressed videos:

* destroy facial texture
* hurt liveness detection
* hurt deepfake detection

---

# STEP 2.11 — Timestamp Extraction

Now your earlier idea comes in.

Extract:

* creation timestamp
* modification timestamp

---

# IMPORTANT REALITY

These are:

```text id="b09jtw"
NOT trustworthy alone
```

because metadata can be edited.

---

# USE THEM AS:

| Usage                 | Importance     |
| --------------------- | -------------- |
| replay hints          | useful         |
| proof of live capture | NOT sufficient |

---

# STEP 2.12 — Freshness Validation

Example rule:

```text id="89m8df"
video must be created within last 2 minutes
```

---

# BUT AGAIN

This is:

```text id="n5h1g6"
supplementary security
```

not core authentication.

---

# STEP 2.13 — Quality Scoring System

Now combine all checks into:

```text id="kr1f56"
video_quality_score
```

---

# EXAMPLE

| Component         | Weight |
| ----------------- | ------ |
| resolution        | 20%    |
| fps               | 20%    |
| frame readability | 20%    |
| duration          | 10%    |
| brightness        | 15%    |
| sharpness         | 15%    |

---

# OUTPUT

```json id="39g6ow"
{
  "quality_score": 0.87
}
```

---

# STEP 2.14 — Structured Analysis Report

VERY IMPORTANT.

Store all results.

Example:

```json id="b5zgjm"
{
  "video_id": "...",
  "metadata": {},
  "validation": {},
  "quality": {},
  "security_flags": []
}
```

---

# WHY?

Later:

* auditing
* debugging
* analytics
* attack detection

all depend on this.

---

# STEP 2.15 — Save Analysis Logs

Store:

```text id="v6i1lp"
logs/video_analysis/
```

---

# SAVE EVERYTHING

Especially:

* failures
* rejected uploads
* suspicious metadata

This becomes VERY useful later.

---

# STEP 2.16 — Build Validation Decision Engine

Final decision:

```json id="i0mwl4"
{
  "accepted": true,
  "reasons": []
}
```

or:

```json id="0x6p6f"
{
  "accepted": false,
  "reasons": [
    "FPS too low",
    "Resolution insufficient"
  ]
}
```

---

# THIS IS IMPORTANT

NEVER:

```text id="tx1o88"
silently reject
```

Structured reasoning is critical.

---

# STEP 2.17 — Create Internal Status Flow

Your pipeline status should now look like:

```text id="l6vbq8"
UPLOADED
↓
VALIDATING
↓
VALID
↓
READY_FOR_FRAME_EXTRACTION
```

---

# WHY?

This becomes essential later when:

* queues exist
* workers exist
* distributed systems exist

---

# STEP 2.18 — TESTING

Test:

| Test               | Expected |
| ------------------ | -------- |
| corrupted mp4      | reject   |
| low FPS            | reject   |
| low resolution     | reject   |
| weird codec        | reject   |
| empty video        | reject   |
| normal phone video | pass     |

---

# HUGE ENGINEERING LESSON

This phase is NOT “just metadata”.

This is:

```text id="v9sp3x"
input trust establishment
```

before AI processing.

Production biometric systems take this VERY seriously.

---

# AFTER THIS PHASE

You will now have:

✅ secure uploads
✅ validated videos
✅ integrity analysis
✅ quality scoring
✅ structured reports
✅ reliable inputs

NOW your AI pipeline can start safely.

---

# NEXT PHASE

# PHASE 3 — Frame Extraction Pipeline

Where we build:

✅ intelligent frame extraction
✅ frame sampling
✅ blur filtering
✅ brightness filtering
✅ frame quality scoring
✅ duplicate frame removal
✅ motion-aware sampling
✅ storage optimization

This is where the system begins preparing:

```text id="m80d1n"
AI-ready facial frames
```

for detection.
