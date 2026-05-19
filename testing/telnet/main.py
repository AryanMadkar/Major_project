import torch
import torch.nn.functional as F

from nemo.collections.asr.models import EncDecSpeakerLabelModel

# =====================================================
# LOAD MODEL
# =====================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")

model = EncDecSpeakerLabelModel.from_pretrained(
    model_name="titanet_large"
)

model = model.to(DEVICE)
model.eval()

# =====================================================
# GET EMBEDDING
# =====================================================

def get_embedding(audio_path):

    with torch.no_grad():

        embedding = model.get_embedding(audio_path)

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

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    similarity = torch.dot(emb1, emb2).item()

    print(f"\nSimilarity Score: {similarity:.4f}")

    if similarity > 0.60:
        print("Same Speaker")
    else:
        print("Different Speaker")

# =====================================================
# TEST
# =====================================================

verify(
    r"D:\majorproject\testing\audio-dataset\Aryan.mp3",
    r"D:\majorproject\testing\audio-dataset\ashlesha2.mp3"
)