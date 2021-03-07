A simple bot to forward sms messages to Telegram.

#Quickstart
1. `pipenv install`
2. `cp config.py.example config.py`
3. Edit `config.py` with the token and chat id from Telegram.
4. Plug the 2g/3g/4g dongle to your machine and identify its port.  On Linux it is usually `/dev/ttyUSB2`.
4. `pipenv run ./sms2tg.py -d /dev/ttyUSB{x}`
