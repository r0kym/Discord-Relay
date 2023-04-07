Discord Relay
=============

Basic bot using [discord.py-self](https://github.com/dolfies/discord.py-self) to relay messages in a channel to a dedicated webhook.

Note: more conveniently you can use the [docker-compose](docker-compose.yml) file to setup environment variables. 

Then use `docker-compose up -d --build` to launch
# Setup
Build the docker image
```shell
docker build -t relay .
```


# Startup

```sh
docker run --rm -d \
  --env "DISCORD_TOKEN=DISCORD_TOKEN" \
  --env "SPY_CHANNELS=[CHANNELS_IDS]" \
  --env "WEBHOOK_ID=WEBHOOK_ID" \
  --env "WEBHOOK_TOKEN=WEBHOOK_TOKEN" \
  --name NAME 
  relay
```
Needs to be started once per tracked discord users but will notify for each channel in `SPY_CHANNELS`.
Put a different `NAME` for each to differentiate them.


# TODO

 - [x] Docker integration
 - [ ] Cleaner code
 - [ ] Multiple clients?