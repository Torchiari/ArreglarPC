import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import datetime
from models.artefacto import Artefacto


def abrir_agregar_arreglo(root, id_cliente, refrescar_cliente, recargar_clientes):
    popup = ttk.Toplevel(root)
    popup.title("Nuevo Arreglo")
    popup.geometry("400x320")

    ttk.Label(popup, text="Detalle del artefacto:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))
    e_detalle = ttk.Entry(popup)
    e_detalle.pack(fill="x", padx=10)

    ttk.Label(popup, text="Estado (Arreglar/Listo):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))
    e_estado = ttk.Entry(popup)
    e_estado.insert(0, "Arreglar")
    e_estado.pack(fill="x", padx=10)

    ttk.Label(popup, text="📅 Fecha:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 3))
    e_fecha = ttk.Entry(popup)
    e_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
    e_fecha.pack(fill="x", padx=10)

    def guardar():
        detalle = e_detalle.get().strip()
        estado = e_estado.get().strip() or "Arreglar"
        fecha = e_fecha.get().strip()

        if not detalle:
            messagebox.showwarning("Atención", "Debe completar el detalle del artefacto.")
            return

        try:
            Artefacto.crear(estado, fecha, detalle, id_cliente)
            messagebox.showinfo("Éxito", "Arreglo agregado correctamente.")
            popup.destroy()
            refrescar_cliente()
            recargar_clientes()
        except Exception as err:
            messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

    ttk.Button(popup, text="Guardar", command=guardar, bootstyle="success").pack(pady=(15, 5))
    ttk.Button(popup, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack()

