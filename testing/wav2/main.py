import torch
import torch.nn.functional as F
import librosa

from speechbrain.pretrained import EncoderClassifier

# =====================================================
# DEVICE
# =====================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")

# =====================================================
# LOAD MODEL
# =====================================================

print("Loading model...")

model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/ecapa"
)

model = model.to(DEVICE)

print("Model loaded!")

# =====================================================
# LOAD AUDIO
# =====================================================

def load_audio(audio_path):

    signal, sr = librosa.load(
        audio_path,
        sr=16000,
        mono=True
    )

    signal = torch.tensor(signal).unsqueeze(0)

    return signal.to(DEVICE)

# =====================================================
# GET EMBEDDING
# =====================================================

def get_embedding(audio_path):

    signal = load_audio(audio_path)

    with torch.no_grad():

        embedding = model.encode_batch(signal)

        embedding = F.normalize(
            embedding,
            p=2,
            dim=-1
        )

    return embedding.squeeze()

# =====================================================
# VERIFY
# =====================================================

def verify(audio1, audio2):

    print("\nExtracting embeddings...")

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    similarity = torch.dot(emb1, emb2).item()

    print(f"\nSimilarity Score: {similarity:.4f}")

    if similarity > 0.70:
        print("Same Speaker")
    else:
        print("Different Speaker")

# =====================================================
# TEST
# =====================================================

verify(
    r"D:\majorproject\testing\audio-dataset\Aryan.wav",
    r"D:\majorproject\testing\audio-dataset\aryan2.mp3"
)