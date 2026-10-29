#!/usr/bin/env bash
# Copia de seguridad SOLO-LECTURA de la config de Steam (pesa unos KB).
# Crea ~/respaldos-konkr/<fecha>/ . No borra ni cambia nada de Steam.
set -u
STEAM=""
for d in "$HOME/.local/share/Steam" "$HOME/.steam/root" "$HOME/.steam/steam"; do
  [ -d "$d/userdata" ] && STEAM="$(readlink -f "$d")" && break
done
[ -z "$STEAM" ] && { echo "No encuentro la carpeta de Steam"; exit 1; }
DEST="$HOME/respaldos-konkr/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$DEST" || exit 1
for f in config/config.vdf config/libraryfolders.vdf steamapps/libraryfolders.vdf; do
  [ -f "$STEAM/$f" ] && mkdir -p "$DEST/$(dirname "$f")" && cp -p "$STEAM/$f" "$DEST/$f"
done
for u in "$STEAM"/userdata/*/; do
  id="$(basename "$u")"
  for f in config/shortcuts.vdf config/localconfig.vdf; do
    [ -f "$u$f" ] && mkdir -p "$DEST/userdata/$id/config" && cp -p "$u$f" "$DEST/userdata/$id/config/"
  done
done
echo "Respaldo en: $DEST"; du -sh "$DEST"
echo "Para restaurar: cierra Steam y copia los archivos de vuelta a su sitio."
