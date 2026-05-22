import requests
files = {
  'audio1': open(r'D:\majorproject\testing\audio-dataset\real_ash.ogg','rb'),
  'audio2': open(r'D:\majorproject\testing\audio-dataset\real_ash_2.ogg','rb'),
}
r = requests.post('http://localhost:8000/verify', files=files)
print(r.status_code, r.text)