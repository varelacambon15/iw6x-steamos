#!/usr/bin/env python3
"""Parche de compatibilidad para iw6-mod.exe en Wine/Proton (Konkr).

El cliente instala un "hook" sobre una importacion de urlmon.dll
(iertutil.dll, ordinal 700). En Windows existe; en Wine urlmon no la importa,
la busqueda devuelve NULL y el programa lee [NULL] y se cae
(EXCEPTION_ACCESS_VIOLATION en RVA 0x316F74).

El parche anade una comprobacion: si el resultado es NULL, se salta el hook.
En Wine ese hook no hace falta.

Uso: python3 parchear_iw6mod.py
  - Abre un cuadro para elegir iw6-mod.exe
  - NO modifica el original: escribe iw6-mod-konkr.exe en la misma carpeta
  - Comprueba antes que los bytes coinciden con la version esperada
Para pruebas sin ventana: python3 parchear_iw6mod.py ruta/iw6-mod.exe
"""
import os
import struct
import sys

# --- Version esperada (base 0x150000000) ---
BASE = 0x150000000
SITE_VA = 0x150316F74            # mov rax,[rbx] ; mov rcx,rbx   (6 bytes)
SITE_ORIG = bytes.fromhex("488b03488bcb")
EPILOGUE_VA = 0x150316FBD        # xor eax,eax ... ret (salida de la funcion)
RETURN_VA = 0x150316F7A          # siguiente instruccion tras las dos parcheadas
CAVE_VA = 0x150426631            # 21 bytes de relleno 0xCC sin uso
CAVE_LEN = 21
SALIDA = "iw6-mod-konkr.exe"


def va_a_offset(datos, va):
    """Convierte una direccion virtual en offset de archivo leyendo las secciones PE."""
    pe = struct.unpack_from("<I", datos, 0x3C)[0]
    nsec = struct.unpack_from("<H", datos, pe + 6)[0]
    tam_opt = struct.unpack_from("<H", datos, pe + 20)[0]
    base = struct.unpack_from("<Q", datos, pe + 24 + 24)[0]
    tabla = pe + 24 + tam_opt
    rva = va - base
    for i in range(nsec):
        _, vsize, vaddr, rsize, roff = struct.unpack_from("<8sIIII", datos, tabla + 40 * i)
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return roff + (rva - vaddr), base
    raise ValueError(f"VA {va:#x} fuera de las secciones")


def rel32(desde_fin, destino):
    return struct.pack("<i", destino - desde_fin)


def construir(datos):
    off_sitio, base = va_a_offset(datos, SITE_VA)
    if base != BASE:
        raise ValueError(f"Base de imagen distinta: {base:#x}")
    if datos[off_sitio:off_sitio + 6] != SITE_ORIG:
        raise ValueError("Los bytes en el punto del parche no coinciden: "
                         "version distinta de iw6-mod.exe. No toco nada.")
    off_cueva, _ = va_a_offset(datos, CAVE_VA)
    if datos[off_cueva:off_cueva + CAVE_LEN] != b"\xcc" * CAVE_LEN:
        raise ValueError("El hueco para el parche no esta libre. No toco nada.")

    c = CAVE_VA
    cueva = (
        b"\x48\x85\xdb"                                   # test rbx,rbx
        + b"\x0f\x84" + rel32(c + 3 + 6, EPILOGUE_VA)     # jz epilogo
        + b"\x48\x8b\x03"                                 # mov rax,[rbx]
        + b"\x48\x8b\xcb"                                 # mov rcx,rbx
        + b"\xe9" + rel32(c + 15 + 5, RETURN_VA)          # jmp de vuelta
    )
    salto = b"\xe9" + rel32(SITE_VA + 5, CAVE_VA) + b"\x90"   # jmp cueva ; nop

    nuevo = bytearray(datos)
    nuevo[off_cueva:off_cueva + len(cueva)] = cueva
    nuevo[off_sitio:off_sitio + 6] = salto
    return bytes(nuevo)


def elegir_archivo():
    if len(sys.argv) > 1:
        return sys.argv[1]
    try:
        import tkinter
        from tkinter import filedialog
        raiz = tkinter.Tk()
        raiz.withdraw()
        ruta = filedialog.askopenfilename(
            title="Elige iw6-mod.exe", filetypes=[("Ejecutables", "*.exe"), ("Todos", "*")])
        raiz.destroy()
        return ruta
    except Exception:
        return input("Ruta de iw6-mod.exe: ").strip()


def aviso(texto):
    print(texto)
    if len(sys.argv) > 1:
        return
    try:
        import tkinter
        from tkinter import messagebox
        raiz = tkinter.Tk()
        raiz.withdraw()
        messagebox.showinfo("Parche iw6-mod", texto)
        raiz.destroy()
    except Exception:
        pass


def main():
    ruta = elegir_archivo()
    if not ruta or not os.path.isfile(ruta):
        return 1
    with open(ruta, "rb") as f:
        datos = f.read()
    try:
        nuevo = construir(datos)
    except ValueError as e:
        aviso(f"No se ha parcheado: {e}")
        return 1
    destino = os.path.join(os.path.dirname(ruta), SALIDA)
    with open(destino, "wb") as f:
        f.write(nuevo)
    aviso(f"Listo. Archivo nuevo:\n{destino}\n\nEl original no se ha tocado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
