#!/usr/bin/env bash
# Devuelve Decky Loader y los plugins aparcados en ~/plugins.off a ~/homebrew/plugins.
# No borra nada. Si un plugin ya existe en destino, lo deja donde esta y avisa.
# Despues, reinicia Steam / vuelve a Modo Juego para que Decky los cargue.
set -u
OFF="$HOME/plugins.off"
DEST="$HOME/homebrew/plugins"

echo "== Plugins aparcados en $OFF:"
if [ -d "$OFF" ] && [ -n "$(ls -A "$OFF" 2>/dev/null)" ]; then
  ls -1 "$OFF"
else
  echo "(vacio o no existe)"
fi

if [ -d "$OFF" ] && [ -d "$DEST" ]; then
  for p in "$OFF"/*/; do
    [ -d "$p" ] || continue
    n="$(basename "$p")"
    if [ -e "$DEST/$n" ]; then
      echo "YA EXISTE en destino, no lo muevo: $n"
    else
      sudo mv -- "$p" "$DEST/$n" && echo "Devuelto: $n"
    fi
  done
elif [ ! -d "$DEST" ]; then
  echo "No existe $DEST: Decky no esta instalado en esta ruta. No muevo nada."
fi

echo "== Servicio de Decky:"
if systemctl list-unit-files plugin_loader.service >/dev/null 2>&1; then
  sudo systemctl enable --now plugin_loader.service
  systemctl is-active plugin_loader.service
else
  echo "No encuentro plugin_loader.service."
fi

echo
echo "== Plugins ahora en $DEST:"
ls -1 "$DEST" 2>/dev/null
echo
echo "Listo. Ahora vuelve a Modo Juego (o reinicia Steam) para ver Decky."
