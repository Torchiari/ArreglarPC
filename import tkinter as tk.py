# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# from tkinter import messagebox
# import mysql.connector

# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "felipe",
#     "database": "arreglopc"
# }

# class ArregloApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("💻 Programa Danel")
#         self.root.geometry("1200x680")
#         self.style = ttk.Style("flatly")  # Tema moderno y limpio

#         # Conexión DB
#         try:
#             self.conn = mysql.connector.connect(**DB_CONFIG)
#             self.cursor = self.conn.cursor(dictionary=True)
#         except mysql.connector.Error as err:
#             messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{err}")
#             root.destroy()
#             return

#         self.crear_interfaz()
#         self.cargar_clientes()

#     def crear_interfaz(self):
#         # ─── Panel superior ───
#         frame_top = ttk.Frame(self.root, padding=(20,15))
#         frame_top.pack(fill="x", padx=15, pady=10)

#         ttk.Label(frame_top, text="🔍 Buscar cliente:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
#         self.var_buscar = ttk.StringVar()
#         entry_buscar = ttk.Entry(frame_top, textvariable=self.var_buscar, width=35, bootstyle="info")
#         entry_buscar.pack(side="left", padx=5)
#         entry_buscar.bind("<Return>", lambda e: self.cargar_clientes())

#         ttk.Button(frame_top, text="Buscar", command=self.cargar_clientes, bootstyle="primary").pack(side="left", padx=5)

#         top_right = ttk.Frame(frame_top)
#         top_right.pack(side="right")
#         ttk.Button(top_right, text="🔄 Refrescar", command=self.cargar_clientes, bootstyle="secondary-outline").pack(side="left", padx=5)
#         ttk.Button(top_right, text="➕ Nuevo Arreglo", command=self.abrir_agregar_popup, bootstyle="success").pack(side="left", padx=5)
#         ttk.Button(top_right, text="🗑️ Eliminar Arreglo", command=self.eliminar_arreglo, bootstyle="danger").pack(side="left", padx=5)

#         # ─── Panel principal ───
#         panel = ttk.Frame(self.root, padding=10)
#         panel.pack(fill="both", expand=True)

#         # ─── Panel izquierdo (Clientes) ───
#         frame_izq = ttk.Frame(panel, bootstyle="secondary", padding=15)
#         frame_izq.pack(side="left", fill="y", padx=(0, 15))

#         ttk.Label(frame_izq, text="👤 Clientes", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
#         ttk.Button(frame_izq, text="➕ Agregar", command=self.abrir_agregar_cliente, bootstyle="success-outline").pack(anchor="w", pady=4)
#         ttk.Button(frame_izq, text="🗑️ Eliminar", command=self.eliminar_cliente, bootstyle="danger-outline").pack(anchor="w", pady=4)

#         columnas_clientes = ("nombre", "artefactos")
#         self.tree_clientes = ttk.Treeview(frame_izq, columns=columnas_clientes, show="headings", height=25)
#         self.tree_clientes.heading("nombre", text="Nombre y Apellido")
#         self.tree_clientes.heading("artefactos", text="N° de Artefactos")
#         self.tree_clientes.column("nombre", width=260)
#         self.tree_clientes.column("artefactos", width=120, anchor="center")
#         self.tree_clientes.pack(fill="y", expand=True, pady=5)
#         self.tree_clientes.bind("<<TreeviewSelect>>", self.on_cliente_select)

#         # ─── Panel derecho (Artefactos) ───
#         frame_der = ttk.Frame(panel, bootstyle="secondary", padding=15)
#         frame_der.pack(side="right", fill="both", expand=True)

#         ttk.Label(frame_der, text="🔧 Artefactos y Arreglos", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

#         columnas = ("tipo", "estado", "fecha", "detalle")
#         self.tree_det = ttk.Treeview(frame_der, columns=columnas, show="headings", height=25)
#         for col in columnas:
#             self.tree_det.heading(col, text=col.capitalize())
#         self.tree_det.column("tipo", width=130, anchor="center")
#         self.tree_det.column("estado", width=120, anchor="center")
#         self.tree_det.column("fecha", width=140, anchor="center")
#         self.tree_det.column("detalle", width=480)
#         self.tree_det.pack(fill="both", expand=True, pady=5)

#         # Colores suaves para estados
#         self.tree_det.tag_configure("listo", background="#d4edda")  # Verde pastel
#         self.tree_det.tag_configure("arreglar", background="#fff3cd")  # Amarillo pastel
#         self.tree_det.tag_configure("meta", background="#e2e3e5")      # Gris claro

#         self.tree_det.bind("<Double-1>", self.on_double_click_detalle)

#     # ─── Funciones principales ───
#     def cargar_clientes(self):
#         filtro = self.var_buscar.get().strip()
#         sql = """
#             SELECT c.Id, c.nombre, COUNT(a.`id.artefacto`) AS cantidad
#             FROM cliente c
#             LEFT JOIN arreglo a ON c.Id = a.`id.cliente`
#         """
#         params = ()
#         if filtro:
#             sql += " WHERE c.nombre LIKE %s"
#             params = (f"%{filtro}%",)
#         sql += " GROUP BY c.Id, c.nombre ORDER BY c.nombre ASC"

#         self.cursor.execute(sql, params)
#         clientes = self.cursor.fetchall()

#         self.tree_clientes.delete(*self.tree_clientes.get_children())
#         for c in clientes:
#             self.tree_clientes.insert("", "end", iid=c["Id"], values=(c["nombre"], c["cantidad"] or 0))

#         self.tree_det.delete(*self.tree_det.get_children())

#     def on_cliente_select(self, _):
#         sel = self.tree_clientes.selection()
#         if not sel:
#             return
#         id_cliente = sel[0]
#         self.mostrar_detalles_cliente(id_cliente)

#     def mostrar_detalles_cliente(self, id_cliente):
#         self.tree_det.delete(*self.tree_det.get_children())
#         self.cursor.execute("""
#             SELECT * FROM artefacto 
#             WHERE Id IN (SELECT `id.artefacto` FROM arreglo WHERE `id.cliente`=%s)
#             ORDER BY Id ASC
#         """, (id_cliente,))
#         artefactos = self.cursor.fetchall()

#         for art in artefactos:
#             tag = "listo" if (art["estado"] or "").lower() == "listo" else "arreglar"
#             self.tree_det.insert("", "end", iid=f"art_{art['Id']}",
#                                  values=("Artefacto", art["estado"], art["fecha"], art["detalle"]),
#                                  tags=(tag,))
#         if not artefactos:
#             self.tree_det.insert("", "end", values=("", "", "", "Este cliente no tiene artefactos o arreglos."), tags=("meta",))

#     def on_double_click_detalle(self, _):
#         sel = self.tree_det.selection()
#         if not sel: return
#         iid = sel[0]
#         if not iid.startswith("art_"): return
#         id_artefacto = iid.split("_")[1]
#         self.cursor.execute("SELECT estado FROM artefacto WHERE Id=%s", (id_artefacto,))
#         estado = self.cursor.fetchone()["estado"]
#         nuevo = "Listo" if (estado or "").lower() != "listo" else "Arreglar"
#         self.cursor.execute("UPDATE artefacto SET estado=%s WHERE Id=%s", (nuevo, id_artefacto))
#         self.conn.commit()
#         self.refrescar_cliente()

#     def refrescar_cliente(self):
#         sel = self.tree_clientes.selection()
#         if sel:
#             self.mostrar_detalles_cliente(sel[0])

#     # ─── Popups mejorados ───
#     def abrir_agregar_popup(self):
#         sel_cliente = self.tree_clientes.selection()
#         if not sel_cliente:
#             messagebox.showwarning("Atención", "Seleccione un cliente para agregar un arreglo.")
#             return

#         id_cliente = sel_cliente[0]
#         popup = ttk.Toplevel(self.root, title="🆕 Nuevo Arreglo", bootstyle="info")
#         popup.geometry("400x300")

#         ttk.Label(popup, text="Detalle del artefacto:").pack(anchor="w", padx=10, pady=5)
#         e_detalle = ttk.Entry(popup); e_detalle.pack(fill="x", padx=10)

#         ttk.Label(popup, text="Estado (Arreglar/Listo):").pack(anchor="w", padx=10, pady=5)
#         e_estado = ttk.Entry(popup); e_estado.insert(0, "Arreglar"); e_estado.pack(fill="x", padx=10)

#         ttk.Label(popup, text="Fecha:").pack(anchor="w", padx=10, pady=5)
#         e_fecha = ttk.Entry(popup); e_fecha.pack(fill="x", padx=10)

#         def guardar():
#             detalle = e_detalle.get().strip()
#             estado = e_estado.get().strip() or "Arreglar"
#             fecha = e_fecha.get().strip()
#             if not detalle:
#                 messagebox.showwarning("Atención", "Debe completar el detalle del artefacto.")
#                 return
#             try:
#                 self.cursor.execute("INSERT INTO artefacto (estado, fecha, detalle) VALUES (%s,%s,%s)", (estado, fecha, detalle))
#                 id_artefacto = self.cursor.lastrowid
#                 self.cursor.execute("INSERT INTO arreglo (`id.cliente`,`id.artefacto`) VALUES (%s,%s)", (id_cliente, id_artefacto))
#                 self.conn.commit()
#                 messagebox.showinfo("Éxito", "Arreglo agregado correctamente.")
#                 popup.destroy()
#                 self.refrescar_cliente()
#                 self.cargar_clientes()
#             except mysql.connector.Error as err:
#                 messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

#         ttk.Button(popup, text="Guardar", command=guardar, bootstyle="success").pack(pady=10)
#         ttk.Button(popup, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack()

#     def abrir_agregar_cliente(self):
#         popup = ttk.Toplevel(self.root, title="Agregar Cliente", bootstyle="info")
#         popup.geometry("350x200")

#         ttk.Label(popup, text="Nombre y Apellido:").pack(anchor="w", padx=10, pady=5)
#         e_nombre = ttk.Entry(popup); e_nombre.pack(fill="x", padx=10)

#         def guardar_cliente():
#             nombre = e_nombre.get().strip()
#             if not nombre:
#                 messagebox.showwarning("Atención", "Debe ingresar un nombre y apellido.")
#                 return
#             try:
#                 self.cursor.execute("INSERT INTO cliente (nombre) VALUES (%s)", (nombre,))
#                 self.conn.commit()
#                 messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
#                 popup.destroy()
#                 self.cargar_clientes()
#             except mysql.connector.Error as err:
#                 messagebox.showerror("Error", f"No se pudo guardar:\n{err}")

#         ttk.Button(popup, text="Guardar", command=guardar_cliente, bootstyle="success").pack(pady=10)
#         ttk.Button(popup, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack()

#     # ─── Métodos eliminar ───
#     def eliminar_arreglo(self):
#         sel = self.tree_det.selection()
#         if not sel:
#             messagebox.showwarning("Atención", "Seleccione un artefacto para eliminar.")
#             return
#         iid = sel[0]
#         if not iid.startswith("art_"):
#             messagebox.showwarning("Atención", "Seleccione una fila de tipo 'Artefacto'.")
#             return
#         id_artefacto = iid.split("_")[1]
#         if not messagebox.askyesno("Confirmar", "¿Eliminar este arreglo y su artefacto asociado?"):
#             return
#         try:
#             self.cursor.execute("DELETE FROM arreglo WHERE `id.artefacto`=%s", (id_artefacto,))
#             self.cursor.execute("DELETE FROM artefacto WHERE Id=%s", (id_artefacto,))
#             self.conn.commit()
#             messagebox.showinfo("Éxito", "Arreglo y artefacto eliminados correctamente.")
#             self.refrescar_cliente()
#             self.cargar_clientes()
#         except mysql.connector.Error as err:
#             messagebox.showerror("Error", f"No se pudo eliminar:\n{err}")

#     def eliminar_cliente(self):
#         sel = self.tree_clientes.selection()
#         if not sel:
#             messagebox.showwarning("Atención", "Seleccione un cliente para eliminar.")
#             return
#         id_cliente = sel[0]
#         if not messagebox.askyesno("Confirmar", "¿Eliminar este cliente y todos sus arreglos y artefactos?"):
#             return
#         try:
#             self.cursor.execute("DELETE FROM artefacto WHERE Id IN (SELECT `id.artefacto` FROM arreglo WHERE `id.cliente`=%s)", (id_cliente,))
#             self.cursor.execute("DELETE FROM arreglo WHERE `id.cliente`=%s", (id_cliente,))
#             self.cursor.execute("DELETE FROM cliente WHERE Id=%s", (id_cliente,))
#             self.conn.commit()
#             messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
#             self.cargar_clientes()
#             self.tree_det.delete(*self.tree_det.get_children())
#         except mysql.connector.Error as err:
#             messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{err}")

# if __name__ == "__main__":
#     root = ttk.Window()
#     app = ArregloApp(root)
#     root.mainloop()
