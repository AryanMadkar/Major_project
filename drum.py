import requests
files = {
  'audio1': open(r'D:\majorproject\testing\audio-dataset\Aryan.wav','rb'),
  'audio2': open(r'D:\majorproject\testing\audio-dataset\aryan2.mp3','rb'),
}
r = requests.post('http://localhost:8000/verify', files=files)
print(r.status_code, r.text)