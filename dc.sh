#!/bin/bash

# Autoffiliate Docker Helper Script

COMMAND=$1
SHIFT_ARGS=${@:2}

case "$COMMAND" in
  up)
    docker compose up -d $SHIFT_ARGS
    ;;
  down)
    docker compose down $SHIFT_ARGS
    ;;
  restart)
    docker compose restart $SHIFT_ARGS
    ;;
  build)
    docker compose build $SHIFT_ARGS
    ;;
  logs)
    docker compose logs -f $SHIFT_ARGS
    ;;
  shell)
    docker compose run --rm app /bin/bash
    ;;
  run)
    docker compose run --rm $SHIFT_ARGS
    ;;
  *)
    echo "Usage: $0 {up|down|restart|build|logs|shell|run}"
    exit 1
    ;;
esac
