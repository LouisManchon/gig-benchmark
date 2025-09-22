# -------- Settings --------
DC  := docker compose
S   ?= backend   # service pour logs/exec
CMD ?= sh        # commande par défaut
SRV ?= backend   # service à scaler
N   ?= 2         # nombre de réplicas

# -------- Basic lifecycle --------

.PHONY: build up down logs ps restart exec run scale

build:
	$(DC) build


build-nc:
	$(DC) build --no-cache

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

logs:
	$(DC) logs -f $(S)

ps:
	$(DC) ps

exec:
	$(DC) exec $(S) $(CMD)

run:
	$(DC) run --rm $(S) $(CMD)

scale:
	$(DC) up -d --scale $(SRV)=$(N)
