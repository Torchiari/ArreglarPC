import ttkbootstrap as ttk
from tkinter import messagebox
from models.cliente import Cliente

def abrir_agregar_cliente(root, recargar_clientes):
    popup = ttk.Toplevel(root, title="Agregar Cliente", bootstyle="info")
    popup.geometry("350x200")

    ttk.Label(popup, text="Nombre y Apellido:").pack(anchor="w", padx=10, pady=5)
    e_nombre = ttk.Entry(popup)
    e_nombre.pack(fill="x", padx=10)

    def guardar_cliente():
        nombre = e_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "Debe ingresar un nombre y apellido.")
            return
        try:
            Cliente.agregar(nombre)
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            popup.destroy()
            recargar_clientes()
        except Exception as err:
            messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

    ttk.Button(popup, text="Guardar", command=guardar_cliente, bootstyle="success").pack(pady=10)
    ttk.Button(popup, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack()
