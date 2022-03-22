Discord Relay
=============

Basic bot using [discord.py-self](https://github.com/dolfies/discord.py-self) to relay messages in a channel to a dedicated webhook.

# Setup
```sh
virtualenv -p python 3.8 venv
. ./venv/bin/activate
pip install -r requirements.txt
```
`deactivate` to leave the virtual environment

# TODO

 - [ ] Cleaner code
 - [ ] Relay channels to different webhooks
   - [ ] Easier webhook handling
   - [ ] Link between webhooks and channels
 - [ ] Multiple spies relay? (Not sure if possible)
