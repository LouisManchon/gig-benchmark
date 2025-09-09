# -------- Settings --------
DC  := docker compose
S   ?= backend   # default service
CMD ?= sh        # default command

# -------- Basic lifecycle --------

.PHONY: build up down logs ps restart exec run scale
build:      ## build all images
	$(DC) build

up:         ## start in detached mode
	$(DC) up -d

down:       ## stop and remove containers
	$(DC) down

restart:    ## restart all services
	$(DC) restart

logs:       ## follow logs (S=service)
	$(DC) logs -f $(S)

ps:         ## list services
	$(DC) ps

# -------- Shortcuts --------
.PHONY: exec run scale
exec:       ## exec into container (S, CMD)
	$(DC) exec $(S) $(CMD)

run:        ## run one-off command (S, CMD)
	$(DC) run --rm $(S) $(CMD)

scale:      ## scale backend (override SRV/N if needed)
	$(DC) up -d --scale $(SRV:=backend)=$(N:=2)
