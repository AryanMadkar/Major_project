import requests
files = {
  'audio1': open(r'D:\majorproject\testing\audio-dataset\ashu_wify.ogg','rb'),
  'audio2': open(r'D:\majorproject\testing\audio-dataset\didi_02.ogg','rb'),
}
r = requests.post('http://localhost:8010/verify', files=files)
print(r.status_code, r.text)