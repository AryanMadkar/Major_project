import requests
import os
import sys

# Edit these paths if needed
AUDIO1 = r"D:\majorproject\testing\audio-dataset\Aryan.wav"
AUDIO2 = r"D:\majorproject\testing\audio-dataset\aryan2.wav"
URL = "http://localhost:8000/verify"

if not os.path.exists(AUDIO1) or not os.path.exists(AUDIO2):
    print("One or both audio files not found. Check paths.")
    sys.exit(1)

with open(AUDIO1, 'rb') as f1, open(AUDIO2, 'rb') as f2:
    files = {
        'audio1': (os.path.basename(AUDIO1), f1, 'audio/wav'),
        'audio2': (os.path.basename(AUDIO2), f2, 'audio/wav')
    }
    try:
        r = requests.post(URL, files=files, timeout=120)
    except Exception as exc:
        print('Request failed:', exc)
        raise

print('Status:', r.status_code)
print('Response:', r.text)

# Optional: check optimized outputs
optimized_dir = os.path.join(os.path.dirname(__file__), '..', 'app', 'uploads', 'optimized')
optimized_dir = os.path.normpath(os.path.abspath(optimized_dir))
base1 = os.path.splitext(os.path.basename(AUDIO1))[0] + '_optimized.wav'
base2 = os.path.splitext(os.path.basename(AUDIO2))[0] + '_optimized.wav'
print('Looking for optimized files in', optimized_dir)
print(base1, 'exists?', os.path.exists(os.path.join(optimized_dir, base1)))
print(base2, 'exists?', os.path.exists(os.path.join(optimized_dir, base2)))
