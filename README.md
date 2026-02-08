# Sistema Integral de Entradas – Python (Consola)

Sistema de gestión de entradas desarrollado en Python que simula un flujo real de venta para un evento.  
Permite registrar ventas con cobro inmediato, controlar cupos por tipo de entrada, gestionar devoluciones, generar estadísticas, mantener un historial de operaciones y exportar reportes.

El proyecto está orientado a la práctica de programación estructurada, uso de estructuras de datos, validaciones y diseño lógico de sistemas.

---

## Descripción general

El sistema funciona por consola y está pensado para representar un escenario real de venta de entradas.  
Todas las ventas se cobran en el momento del registro. Si el cliente no paga o el pago es insuficiente, la venta no se registra.

El operador inicia sesión al comenzar y todas las acciones quedan asociadas a esa sesión.

---

## Funcionalidades

### Operador
- Registro de nombre y apellido del operador.
- Registro automático de fecha y hora de inicio de sesión.
- Todas las operaciones quedan registradas en el historial.

---

### Venta de entradas
- Registro de ventas con cobro inmediato.
- Cada venta incluye:
  - ID único autoincremental.
  - Nombre y apellido del cliente.
  - Edad.
  - Tipo de entrada (General, Estudiante o VIP).
  - Precio final (incluye descuento si corresponde).
  - Monto pagado.
  - Método de pago (Efectivo o Transferencia).
  - Vuelto.
  - Fecha y hora del cobro.
  - Estado de la venta.

No existen ventas pendientes.  
Si el cliente no compra o el pago no alcanza, la operación se cancela sin registrarse.

---

### Métodos de pago
- Efectivo.
- Transferencia.

El método de pago se almacena y se muestra en resúmenes, estadísticas y reportes exportados.

---

### Control de cupos
- Cupo inicial de 100 entradas por tipo:
  - General
  - Estudiante
  - VIP
- El cupo se descuenta únicamente cuando la venta se concreta.
- En caso de devolución, el cupo se libera automáticamente.

---

### Devoluciones
- Devolución por ID de venta.
- Solo se permite devolver ventas cobradas.
- Al realizar una devolución:
  - Se cambia el estado a `DEVUELTA`.
  - Se registra fecha y hora de la devolución.
  - Se devuelve el monto correspondiente según la política del sistema.
  - Se ajusta la recaudación total.
  - Se libera el cupo correspondiente.
  - Se registra la operación en el historial.

---

### Resumen y reportes
- Resumen general con:
  - Total de ventas registradas.
  - Ventas activas.
  - Ventas devueltas.
  - Recaudación total.
  - Cupos disponibles.
- Visualización opcional del detalle completo de las ventas.
- Exportación del resumen a archivos `.txt`.

Los archivos de salida `.txt` no se incluyen en el repositorio (definidos en `.gitignore`).

---

### Estadísticas
- Recaudación por tipo de entrada.
- Cantidad de ventas por tipo.
- Promedio de edad por tipo de entrada.
- Tipo de entrada más vendida.
- Cliente de menor y mayor edad registrados.

---

### Historial de operaciones
- Registro cronológico de todas las acciones del operador:
  - Ventas realizadas.
  - Ventas canceladas o fallidas.
  - Devoluciones.
  - Exportaciones de reportes.
  - Cierre de caja.
- Cada operación se almacena con fecha y hora.

---

### Cierre de caja (simulado)
- Visualización del estado final del sistema.
- Recaudación total.
- Cupos restantes.
- Posibilidad de exportar el cierre de caja a un archivo `.txt`.

---

## Tecnologías utilizadas
- Python 3.x
- Librerías estándar:
  - `datetime`

No se utilizan dependencias externas.

---

## Ejecución del programa
