import os

workers = 2

threads = 4

timeout = 120

bind = f"0.0.0.0:{int(os.getenv('DEEPSPEAKER_PORT', '8004'))}"
