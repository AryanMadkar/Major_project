import os

workers = 2

threads = 4

timeout = 120

bind = f"0.0.0.0:{int(os.getenv('ESPACA_PORT', '8000'))}"