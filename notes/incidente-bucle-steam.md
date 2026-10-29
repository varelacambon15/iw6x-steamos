# Incidente: bucle de arranque de Steam (2026-10-29)
Causa: el wrapper hacia `[ -f steam_appid.txt ] || echo 209160 > steam_appid.txt` con
ruta relativa; cayo en la carpeta del cliente de Steam y Steam se identificaba como
Ghosts y se reiniciaba en bucle. Solucion: borrar ese `steam_appid.txt`.
Leccion: ante un fallo tras un cambio, mirar primero `find -newer` de lo modificado.
