# iw6x-steamos

Llevar **Call of Duty: Ghosts + IW6-Mod (AlterWare)** a la **KONKR Pocket FIT**
(Snapdragon 8 Gen 3, SteamOS ARM de hashtagbasit, Proton ARM64 + FEX).

> Repo publico: aqui NO se suben juegos, exe ni DLL, solo scripts y notas.
> Hace falta tener Ghosts en tu propia cuenta de Steam.

## Reglas de seguridad (aprendidas por las malas)
1. Ningun script escribe fuera de la carpeta del juego o de `~/respaldos-konkr`.
2. Nunca crear archivos con rutas relativas. Un `steam_appid.txt` en la carpeta
   del cliente de Steam provoco un bucle de arranque (ver `notes/incidente-bucle-steam.md`).
3. Antes de cada sesion de pruebas: `tools/respaldo_steam.sh`.
4. Probar siempre desde **modo escritorio**; modo juego solo cuando funcione.

## Estado
- `iw6-mod.exe` (6.347.776 bytes) se cae en RVA `0x316F74`: busca el ordinal 700
  de `iertutil.dll` en `urlmon.dll`; Wine no lo tiene, devuelve NULL y hay un
  `mov rax,[rbx]` sin comprobar. `tools/parchear_iw6mod.py` crea
  `iw6-mod-konkr.exe` con una comprobacion de NULL. **Sin probar aun en la consola.**
- Pendiente: probar el parche, ver el siguiente fallo (si lo hay).

## Uso
1. En la Konkr: `bash tools/respaldo_steam.sh`
2. `python3 tools/parchear_iw6mod.py` (elige tu `iw6-mod.exe`; genera `iw6-mod-konkr.exe` al lado).
3. Steam > Anadir juego no-Steam > `iw6-mod-konkr.exe`; compatibilidad **Proton 11.0 (ARM64)**;
   Iniciar en = carpeta del juego; opciones de lanzamiento:
   `/home/steamos/iw6x-steamos/tools/ghosts_wrapper.sh konkr-game compat %command%`
