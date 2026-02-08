"""
Sistema Integral de Entradas para Evento (Consola) - Cobro SOLO al registrar

Cambios aplicados (según lo pedido):
✅ La venta se cobra en el momento. Si no paga / paga insuficiente -> NO se registra.
✅ Se eliminó "cobrar por ID" y "pendientes" (no existen).
✅ "Cancelar" se convirtió en DEVOLUCIÓN/REEMBOLSO por ID (para ventas ya cobradas).
✅ Se agrega método de pago: EFECTIVO o TRANSFERENCIA.

Se mantiene:
- Operador + inicio de sesión
- Cupos por tipo
- Resumen + export TXT
- Buscar por apellido
- Estadísticas
- Historial
- Cierre de caja (simulado)
"""

from datetime import datetime


# =========================
# Helpers (validación / UI)
# =========================
def ahora_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pedir_texto_no_vacio(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("⚠️  No puede estar vacío.")
        texto = input(mensaje).strip()
    return texto


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("⚠️  Ingrese un número entero válido.")


def pedir_entero_en_rango(mensaje, minimo, maximo):
    while True:
        n = pedir_entero(mensaje)
        if n < minimo or n > maximo:
            print(f"⚠️  Número inválido. Debe estar entre {minimo} y {maximo}.")
        else:
            return n


def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("⚠️  Ingrese un número válido (ej: 5000 o 5000.50).")


def pedir_monto_positivo(mensaje):
    while True:
        monto = pedir_float(mensaje)
        if monto <= 0:
            print("⚠️  El monto debe ser mayor a 0.")
        else:
            return monto


def confirmar_sn(mensaje):
    r = input(mensaje + " (S/N): ").strip().upper()
    while r != "S" and r != "N":
        r = input("⚠️  Responda S o N: ").strip().upper()
    return r == "S"


def print_titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def pausar():
    input("\nPresione ENTER para continuar...")


# =========================
# Dominio: Entradas / Precios
# =========================
def pedir_tipo_entrada():
    print("\nTipos de entrada:")
    print("1 - General")
    print("2 - Estudiante")
    print("3 - VIP")
    return pedir_entero_en_rango("Seleccione tipo (1-3): ", 1, 3)


def nombre_tipo_entrada(tipo):
    if tipo == 1:
        return "General"
    elif tipo == 2:
        return "Estudiante"
    else:
        return "VIP"


def precio_base_por_tipo(tipo_entrada):
    if tipo_entrada == "General":
        return 5000.0
    elif tipo_entrada == "Estudiante":
        return 3000.0
    else:
        return 9000.0


def calcular_precio(tipo_entrada, edad):
    precio = precio_base_por_tipo(tipo_entrada)
    if edad >= 60:
        precio = precio * 0.8
    return float(precio)


def pedir_metodo_pago():
    print("\nMétodo de pago:")
    print("1 - Efectivo")
    print("2 - Transferencia")
    op = pedir_entero_en_rango("Seleccione método (1-2): ", 1, 2)
    if op == 1:
        return "EFECTIVO"
    return "TRANSFERENCIA"


# =========================
# Data / Operaciones
# =========================
def crear_estado_inicial():
    return {
        "operador": {
            "nombre": "",
            "apellido": "",
            "inicio_sesion": "",
        },
        "cupos": {
            "General": 100,
            "Estudiante": 100,
            "VIP": 100,
        },
        "usuarios": [],
        "next_id": 1,
        "recaudacion_total": 0.0,
        "entradas_cobradas": 0,
        "historial": []
    }


def log_operacion(estado, texto):
    estado["historial"].append(f"[{ahora_str()}] {texto}")


def mostrar_cupos(cupos):
    print("\nCUPOS DISPONIBLES:")
    print(f"  General:    {cupos['General']}")
    print(f"  Estudiante: {cupos['Estudiante']}")
    print(f"  VIP:        {cupos['VIP']}")


def crear_usuario(estado, nombre, apellido, edad, entrada, precio, monto_pagado, metodo_pago):
    u = {
        "id": estado["next_id"],
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "entrada": entrada,
        "precio": float(precio),
        "monto_pagado": float(monto_pagado),
        "metodo_pago": metodo_pago,                 # NUEVO
        "vuelto": float(monto_pagado - precio),
        "hora_cobro": ahora_str(),
        "estado": "COBRADA",                        # solo se registra si compra
        "hora_devolucion": "",                      # NUEVO
        "monto_devuelto": 0.0                       # NUEVO
    }
    estado["next_id"] += 1
    return u


def buscar_usuario_por_id(usuarios, uid):
    for u in usuarios:
        if u["id"] == uid:
            return u
    return None


def contar_por_estado(usuarios):
    cob = 0
    dev = 0
    for u in usuarios:
        if u["estado"] == "COBRADA":
            cob += 1
        elif u["estado"] == "DEVUELTA":
            dev += 1
    return cob, dev


# =========================
# Export / Reportes
# =========================
def generar_resumen_texto(estado):
    op = estado["operador"]
    usuarios = estado["usuarios"]
    cupos = estado["cupos"]

    cobradas, devueltas = contar_por_estado(usuarios)

    lineas = []
    lineas.append("SISTEMA INTEGRAL DE ENTRADAS - RESUMEN")
    lineas.append("=" * 60)
    lineas.append(f"Operador: {op['nombre']} {op['apellido']}")
    lineas.append(f"Inicio sesión: {op['inicio_sesion']}")
    lineas.append(f"Generado: {ahora_str()}")
    lineas.append("")
    lineas.append(f"Total ventas registradas: {len(usuarios)}")
    lineas.append(f"Cobradas (activas): {cobradas} | Devueltas: {devueltas}")
    lineas.append(f"Recaudación total: {estado['recaudacion_total']:.2f}")
    lineas.append("")
    lineas.append("Cupos restantes:")
    lineas.append(f"  General:    {cupos['General']}")
    lineas.append(f"  Estudiante: {cupos['Estudiante']}")
    lineas.append(f"  VIP:        {cupos['VIP']}")
    lineas.append("")
    lineas.append("Detalle de ventas:")
    lineas.append("-" * 60)
    for u in usuarios:
        lineas.append(
            f"ID {u['id']} | {u['apellido']}, {u['nombre']} | Edad {u['edad']} | "
            f"{u['entrada']} | Estado {u['estado']} | Precio {u['precio']:.2f} | "
            f"Pagado {u['monto_pagado']:.2f} ({u['metodo_pago']}) | "
            f"Vuelto {u['vuelto']:.2f} | Hora cobro {u['hora_cobro'] or '-'} | "
            f"Devolución {u['monto_devuelto']:.2f} | Hora devolución {u['hora_devolucion'] or '-'}"
        )
    lineas.append("-" * 60)
    lineas.append("")
    lineas.append("Historial de operaciones:")
    lineas.append("-" * 60)
    if len(estado["historial"]) == 0:
        lineas.append("(sin operaciones)")
    else:
        for h in estado["historial"]:
            lineas.append(h)
    lineas.append("-" * 60)

    return "\n".join(lineas)


def exportar_resumen_txt(estado, nombre_archivo):
    contenido = generar_resumen_texto(estado)
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"✅ Exportado correctamente: {nombre_archivo}")
        log_operacion(estado, f"Exportó resumen a '{nombre_archivo}'")
    except Exception as e:
        print("❌ Error al exportar:", e)


# =========================
# Estadísticas
# =========================
def estadisticas(usuarios):
    # Nota: recaudación por tipo considera SOLO COBRADAS activas (no devueltas)
    rec_por_tipo = {"General": 0.0, "Estudiante": 0.0, "VIP": 0.0}
    cont_por_tipo = {"General": 0, "Estudiante": 0, "VIP": 0}

    suma_edad = {"General": 0, "Estudiante": 0, "VIP": 0}
    cant_edad = {"General": 0, "Estudiante": 0, "VIP": 0}

    min_u = None
    max_u = None

    for u in usuarios:
        t = u["entrada"]

        cont_por_tipo[t] += 1
        suma_edad[t] += u["edad"]
        cant_edad[t] += 1

        if u["estado"] == "COBRADA":
            rec_por_tipo[t] += u["precio"]

        if min_u is None or u["edad"] < min_u["edad"]:
            min_u = u
        if max_u is None or u["edad"] > max_u["edad"]:
            max_u = u

    mas_vendida = None
    max_cont = -1
    for t in ["General", "Estudiante", "VIP"]:
        if cont_por_tipo[t] > max_cont:
            max_cont = cont_por_tipo[t]
            mas_vendida = t

    prom_edad = {"General": 0.0, "Estudiante": 0.0, "VIP": 0.0}
    for t in ["General", "Estudiante", "VIP"]:
        if cant_edad[t] > 0:
            prom_edad[t] = suma_edad[t] / cant_edad[t]

    return rec_por_tipo, cont_por_tipo, prom_edad, min_u, max_u, mas_vendida


# =========================
# Casos de uso (opciones)
# =========================
def opcion_nueva_venta(estado):
    print_titulo("NUEVA VENTA (REGISTRO + COBRO)")
    mostrar_cupos(estado["cupos"])

    nombre = pedir_texto_no_vacio("Nombre: ")
    apellido = pedir_texto_no_vacio("Apellido: ")
    edad = pedir_entero_en_rango("Edad (1-120): ", 1, 120)

    if edad < 16:
        print("⛔ Acceso denegado: menor de 16 años. No se registra.")
        log_operacion(estado, f"Venta denegada (menor de 16): {apellido}, {nombre}, edad {edad}")
        return

    tipo = pedir_tipo_entrada()
    entrada = nombre_tipo_entrada(tipo)

    if estado["cupos"][entrada] <= 0:
        print(f"⛔ No hay cupo disponible para {entrada}.")
        log_operacion(estado, f"Venta sin cupo ({entrada}): {apellido}, {nombre}")
        return

    precio = calcular_precio(entrada, edad)
    print(f"\nEntrada: {entrada} | Precio final: {precio:.2f}")

    if not confirmar_sn("¿El cliente compra y paga ahora?"):
        print("❎ No compró. No se registra.")
        log_operacion(estado, f"No se registró (no compró): {apellido}, {nombre}, {entrada}, precio {precio:.2f}")
        return

    metodo = pedir_metodo_pago()
    monto = pedir_monto_positivo("Monto pagado: ")

    if monto < precio:
        faltan = precio - monto
        print(f"❌ Pago insuficiente. Faltan: {faltan:.2f}. No se registra.")
        log_operacion(estado, f"No se registró (pago insuficiente): {apellido}, {nombre}, pagó {monto:.2f}, faltan {faltan:.2f}")
        return

    if not confirmar_sn(f"Confirmar venta por {precio:.2f} (pagó {monto:.2f} - {metodo})?"):
        print("❎ Venta cancelada por el operador. No se registra.")
        log_operacion(estado, f"Venta cancelada por operador: {apellido}, {nombre}")
        return

    u = crear_usuario(estado, nombre, apellido, edad, entrada, precio, monto, metodo)
    estado["usuarios"].append(u)

    estado["cupos"][entrada] -= 1
    estado["recaudacion_total"] += precio
    estado["entradas_cobradas"] += 1

    print(f"✅ Venta registrada. ID {u['id']} | Vuelto: {u['vuelto']:.2f}")
    log_operacion(
        estado,
        f"Venta ID {u['id']} ({entrada}) {apellido}, {nombre} | precio {precio:.2f} | pagó {monto:.2f} ({metodo}) | vuelto {u['vuelto']:.2f}"
    )


def opcion_devolucion_por_id(estado):
    print_titulo("DEVOLUCIÓN / REEMBOLSO POR ID")

    uid = pedir_entero("Ingrese el ID: ")
    u = buscar_usuario_por_id(estado["usuarios"], uid)
    if u is None:
        print("❌ No existe una venta con ese ID.")
        return

    if u["estado"] != "COBRADA":
        print(f"⚠️  No se puede devolver. Estado actual: {u['estado']}")
        return

    print(
        f"ID {u['id']} | {u['nombre']} {u['apellido']} | {u['entrada']} | "
        f"Precio: {u['precio']:.2f} | Pagó: {u['monto_pagado']:.2f} ({u['metodo_pago']})"
    )

    # Política simple: se devuelve el "precio" (lo que fue recaudación).
    monto_a_devolver = u["precio"]
    print(f"\nMonto a devolver (por política del sistema): {monto_a_devolver:.2f}")

    if not confirmar_sn("¿Confirmar devolución? (sube cupo y resta recaudación)"):
        print("❎ Devolución cancelada.")
        log_operacion(estado, f"Devolución cancelada por operador para ID {u['id']}")
        return

    # Aplicar devolución
    u["estado"] = "DEVUELTA"
    u["hora_devolucion"] = ahora_str()
    u["monto_devuelto"] = float(monto_a_devolver)

    # Ajustes de caja y cupos
    estado["cupos"][u["entrada"]] += 1
    estado["recaudacion_total"] -= monto_a_devolver

    # Mantener coherencia del contador "entradas_cobradas"
    if estado["entradas_cobradas"] > 0:
        estado["entradas_cobradas"] -= 1

    print("✅ Devolución realizada. Cupo liberado y caja ajustada.")
    log_operacion(
        estado,
        f"Devolución ID {u['id']} | devolvió {monto_a_devolver:.2f} | cupo +1 {u['entrada']}"
    )


def opcion_resumen_export(estado):
    print_titulo("RESUMEN (Y EXPORT)")
    op = estado["operador"]
    usuarios = estado["usuarios"]
    cobradas, devueltas = contar_por_estado(usuarios)

    print(f"Operador: {op['nombre']} {op['apellido']}")
    print(f"Inicio sesión: {op['inicio_sesion']}")
    print(f"Ahora: {ahora_str()}")
    print("")
    print(f"Total ventas registradas: {len(usuarios)}")
    print(f"Cobradas (activas): {cobradas}")
    print(f"Devueltas: {devueltas}")
    print(f"Recaudación total: {estado['recaudacion_total']:.2f}")

    mostrar_cupos(estado["cupos"])

    if confirmar_sn("¿Mostrar detalle completo?"):
        print("\nDETALLE:")
        print("-" * 70)
        for u in usuarios:
            print(
                f"ID {u['id']:>3} | {u['apellido']}, {u['nombre']} | "
                f"Edad {u['edad']:>3} | {u['entrada']:<10} | "
                f"{u['estado']:<8} | Precio {u['precio']:>8.2f} | "
                f"Pagó {u['monto_pagado']:>8.2f} ({u['metodo_pago']}) | "
                f"Vuelto {u['vuelto']:>8.2f} | Cobro {u['hora_cobro'] or '-'} | "
                f"Dev {u['monto_devuelto']:>8.2f} | HoraDev {u['hora_devolucion'] or '-'}"
            )
        print("-" * 70)

    if confirmar_sn("¿Exportar a TXT?"):
        nombre_archivo = pedir_texto_no_vacio("Nombre del archivo (ej: resumen.txt): ")
        if not nombre_archivo.lower().endswith(".txt"):
            nombre_archivo += ".txt"
        exportar_resumen_txt(estado, nombre_archivo)


def opcion_buscar_por_apellido(estado):
    print_titulo("BUSCAR POR APELLIDO")
    buscado = pedir_texto_no_vacio("Apellido a buscar: ").strip().lower()

    encontrados = []
    for u in estado["usuarios"]:
        if u["apellido"].strip().lower() == buscado:
            encontrados.append(u)

    if len(encontrados) == 0:
        print("❌ No se encontraron ventas con ese apellido.")
        return

    print(f"✅ Encontrados {len(encontrados)} registro(s):")
    print("-" * 70)
    for u in encontrados:
        print(
            f"ID {u['id']:>3} | {u['apellido']}, {u['nombre']} | Edad {u['edad']} | "
            f"{u['entrada']} | {u['estado']} | Pagó {u['monto_pagado']:.2f} ({u['metodo_pago']})"
        )
    print("-" * 70)


def opcion_estadisticas(estado):
    print_titulo("ESTADÍSTICAS")
    usuarios = estado["usuarios"]
    if len(usuarios) == 0:
        print("⚠️  No hay datos para calcular estadísticas.")
        return

    rec_por_tipo, cont_por_tipo, prom_edad, min_u, max_u, mas_vendida = estadisticas(usuarios)

    print("Recaudación por tipo (solo cobradas activas):")
    for t in ["General", "Estudiante", "VIP"]:
        print(f"  {t:<10}: {rec_por_tipo[t]:.2f}")

    print("\nVentas por tipo (incluye devueltas):")
    for t in ["General", "Estudiante", "VIP"]:
        print(f"  {t:<10}: {cont_por_tipo[t]}")

    print("\nPromedio de edad por tipo:")
    for t in ["General", "Estudiante", "VIP"]:
        print(f"  {t:<10}: {prom_edad[t]:.2f}")

    print(f"\nEntrada más vendida (por registros): {mas_vendida}")

    if min_u is not None and max_u is not None:
        print("\nExtremos de edad:")
        print(f"  Más joven: ID {min_u['id']} - {min_u['nombre']} {min_u['apellido']} ({min_u['edad']} años)")
        print(f"  Más viejo: ID {max_u['id']} - {max_u['nombre']} {max_u['apellido']} ({max_u['edad']} años)")

    if confirmar_sn("\n¿Exportar resumen a TXT (incluye historial)?"):
        nombre_archivo = pedir_texto_no_vacio("Nombre del archivo (ej: estadisticas.txt): ")
        if not nombre_archivo.lower().endswith(".txt"):
            nombre_archivo += ".txt"
        exportar_resumen_txt(estado, nombre_archivo)


def opcion_historial(estado):
    print_titulo("HISTORIAL")
    if len(estado["historial"]) == 0:
        print("(sin operaciones)")
        return
    for h in estado["historial"]:
        print(h)


def opcion_cierre_caja(estado):
    print_titulo("CIERRE DE CAJA (SIMULADO)")
    op = estado["operador"]
    usuarios = estado["usuarios"]
    cobradas, devueltas = contar_por_estado(usuarios)

    print(f"Operador: {op['nombre']} {op['apellido']}")
    print(f"Inicio sesión: {op['inicio_sesion']}")
    print(f"Cierre: {ahora_str()}")
    print("")
    print(f"Ventas registradas: {len(usuarios)} | Activas: {cobradas} | Devueltas: {devueltas}")
    print(f"Recaudación total: {estado['recaudacion_total']:.2f}")
    mostrar_cupos(estado["cupos"])

    if confirmar_sn("\n¿Exportar cierre de caja a TXT?"):
        nombre_archivo = f"cierre_caja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        exportar_resumen_txt(estado, nombre_archivo)

    log_operacion(estado, "Realizó cierre de caja (simulado)")


# =========================
# Menú principal (limpio)
# =========================
def mostrar_menu():
    print("\n" + "=" * 70)
    print("1 - Nueva venta")
    print("2 - Devolución por ID")
    print("3 - Resumen / Exportar")
    print("4 - Buscar por apellido")
    print("5 - Estadísticas")
    print("6 - Historial")
    print("7 - Cierre de caja")
    print("8 - Salir")
    print("=" * 70)


def main():
    estado = crear_estado_inicial()

    print_titulo("SISTEMA INTEGRAL DE ENTRADAS")
    estado["operador"]["nombre"] = pedir_texto_no_vacio("Nombre del operador: ")
    estado["operador"]["apellido"] = pedir_texto_no_vacio("Apellido del operador: ")
    estado["operador"]["inicio_sesion"] = ahora_str()

    log_operacion(
        estado,
        f"Inicio de sesión operador: {estado['operador']['apellido']}, {estado['operador']['nombre']}"
    )

    while True:
        mostrar_menu()
        opcion = pedir_entero_en_rango("Elegí una opción (1-8): ", 1, 8)

        if opcion == 1:
            opcion_nueva_venta(estado)
            pausar()

        elif opcion == 2:
            opcion_devolucion_por_id(estado)
            pausar()

        elif opcion == 3:
            opcion_resumen_export(estado)
            pausar()

        elif opcion == 4:
            opcion_buscar_por_apellido(estado)
            pausar()

        elif opcion == 5:
            opcion_estadisticas(estado)
            pausar()

        elif opcion == 6:
            opcion_historial(estado)
            pausar()

        elif opcion == 7:
            opcion_cierre_caja(estado)
            pausar()

        else:
            print_titulo("SALIENDO")
            print("Gracias por usar el sistema.")
            if confirmar_sn("¿Desea exportar un resumen final antes de salir?"):
                nombre_archivo = f"resumen_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                exportar_resumen_txt(estado, nombre_archivo)
            log_operacion(estado, "Cerró el sistema")
            break


if __name__ == "__main__":
    main()