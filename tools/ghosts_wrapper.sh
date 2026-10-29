#!/usr/bin/env bash
# Wrapper MINIMO para opciones de lanzamiento de Steam. Uso:
#   /home/steamos/iw6x-steamos/tools/ghosts_wrapper.sh [konkr-game compat] %command%
# SEGURIDAD: no crea ni modifica ningun archivo fuera de ~/ghosts_wrapper.log.
# (La version anterior escribia steam_appid.txt con ruta relativa y rompio Steam.
#  NUNCA escribir en el directorio de trabajo: puede ser la carpeta de Steam.)
LOG="$HOME/ghosts_wrapper.log"
{
  echo "=== $(date) ==="
  echo "cwd: $(pwd)"
  echo "cmd: $*"
} >>"$LOG" 2>&1
exec "$@"
