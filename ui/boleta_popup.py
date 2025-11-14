import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import datetime
from models.boleta import Boleta
from utils.generar_pdf_boleta import generar_pdf_boleta


def abrir_generar_boleta(root, id_cliente, id_artefacto, detalle_existente, refrescar_cliente):

    popup = ttk.Toplevel(root)
    popup.title("Generar Boleta")
    popup.geometry("420x360")
    popup.resizable(False, False)

    ttk.Label(popup, text="Detalle del Arreglo:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))

    # 👉 Campo editable con el detalle existente
    e_detalle = ttk.Entry(popup)
    e_detalle.insert(0, detalle_existente)
    e_detalle.pack(fill="x", padx=10)

    ttk.Label(popup, text="Valor ($):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))
    e_valor = ttk.Entry(popup)
    e_valor.pack(fill="x", padx=10)

    ttk.Label(popup, text="Fecha:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))
    e_fecha = ttk.Entry(popup)
    e_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
    e_fecha.pack(fill="x", padx=10)

    def guardar_boleta():
        detalle_final = e_detalle.get().strip()
        valor = e_valor.get().strip()
        fecha = e_fecha.get().strip()

        if not valor:
            messagebox.showwarning("Atención", "Debe ingresar un valor.")
            return

        try:
            # Guardar en BD
            Boleta.crear(fecha, valor, detalle_final, id_cliente, id_artefacto)

            # 👉 Obtener nombre del cliente para usarlo en el PDF
            from models.cliente import Cliente
            datos_cliente = Cliente.obtener_por_id(id_cliente)
            nombre_cliente = datos_cliente["nombre"]

            # 👉 Generar PDF con los parámetros correctos
            generar_pdf_boleta(
                nombre_cliente=nombre_cliente,
                fecha=fecha,
                detalle=detalle_final,
                valor=valor,
                id_cliente=id_cliente,
                id_artefacto=id_artefacto
            )

            messagebox.showinfo("Éxito", "Boleta generada correctamente.")
            popup.destroy()
            refrescar_cliente()

        except Exception as err:
            messagebox.showerror("Error", f"No se pudo generar la boleta:\n{err}")

    ttk.Button(popup, text="Generar Boleta", command=guardar_boleta, bootstyle="success").pack(pady=15)
    ttk.Button(popup, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack()
