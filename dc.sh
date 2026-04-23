#!/bin/bash

# Standard dc.sh for Docker Compose management

case "$1" in
  up)
    docker compose up -d
    ;;
  down)
    docker compose down
    ;;
  restart)
    docker compose restart
    ;;
  build)
    docker compose build
    ;;
  logs)
    docker compose logs -f
    ;;
  shell)
    docker compose exec app bash
    ;;
  *)
    echo "Usage: $0 {up|down|restart|build|logs|shell}"
    exit 1
    ;;
esac
