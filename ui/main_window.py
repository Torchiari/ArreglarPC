import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, HORIZONTAL
from models.cliente import Cliente
from models.artefacto import Artefacto
from ui.arreglo_popup import abrir_agregar_arreglo

class ArregloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💻 Programa Danel")
        self.root.geometry("1200x700")
        self.style = ttk.Style("darkly")  # Tema oscuro elegante

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        # --- HEADER SUPERIOR ---
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text="🔍 Buscar cliente:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(10, 5))
        self.var_buscar = ttk.StringVar()
        entry_buscar = ttk.Entry(header, textvariable=self.var_buscar, width=35, bootstyle="info")
        entry_buscar.pack(side="left", padx=5)
        entry_buscar.bind("<Return>", lambda e: self.cargar_clientes())

        ttk.Button(header, text="Buscar", command=self.cargar_clientes, bootstyle="primary").pack(side="left", padx=5)

        btn_group = ttk.Frame(header)
        btn_group.pack(side="right")
        ttk.Button(btn_group, text="Refrescar", command=self.cargar_clientes, bootstyle="secondary-outline").pack(side="left", padx=5)
        ttk.Button(btn_group, text="➕ Nuevo Arreglo", command=self.abrir_popup_arreglo, bootstyle="success-outline").pack(side="left", padx=5)
        ttk.Button(btn_group, text="🗑️ Eliminar Arreglo", command=self.eliminar_arreglo, bootstyle="danger-outline").pack(side="left", padx=5)

        # --- PANEL PRINCIPAL ---
        panel = ttk.Panedwindow(self.root, orient=HORIZONTAL)
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        # --- PANEL IZQUIERDO: CLIENTES ---
        frame_izq = ttk.Labelframe(panel, text="👤 Clientes", bootstyle="white", padding=10)
        panel.add(frame_izq, weight=1)

        ttk.Button(frame_izq, text="➕ Agregar Cliente", command=self.abrir_popup_cliente, bootstyle="success-outline").pack(fill="x", pady=4)
        ttk.Button(frame_izq, text="🗑️ Eliminar Cliente", command=self.eliminar_cliente, bootstyle="danger-outline").pack(fill="x", pady=4)

        columnas_clientes = ("nombre", "artefactos")
        self.tree_clientes = ttk.Treeview(frame_izq, columns=columnas_clientes, show="headings", height=22)
        self.tree_clientes.heading("nombre", text="Nombre y Apellido", anchor="center")
        self.tree_clientes.heading("artefactos", text="N° de Artefactos", anchor="center")

        self.tree_clientes.column("nombre", anchor="center", width=220)
        self.tree_clientes.column("artefactos", anchor="center", width=130)

        self.tree_clientes.pack(fill="both", expand=True, pady=(10, 0))
        self.tree_clientes.bind("<<TreeviewSelect>>", self.on_cliente_select)

        # Alternar colores en filas
        self.tree_clientes.tag_configure("oddrow", background="#1e1e1e")
        self.tree_clientes.tag_configure("evenrow", background="#2b2b2b")

        # --- PANEL DERECHO: ARTEFACTOS ---
        frame_der = ttk.Labelframe(panel, text="Artefactos y Arreglos", bootstyle="white", padding=10)
        panel.add(frame_der, weight=3)

        columnas = ("estado", "fecha", "detalle")
        self.tree_det = ttk.Treeview(frame_der, columns=columnas, show="headings", height=22)

        self.tree_det.heading("estado", text="Estado", anchor="center")
        self.tree_det.heading("fecha", text="Fecha", anchor="center")
        self.tree_det.heading("detalle", text="Detalle", anchor="center")

        self.tree_det.column("estado", anchor="center", width=120)
        self.tree_det.column("fecha", anchor="center", width=120)
        self.tree_det.column("detalle", anchor="center", width=400)

        self.tree_det.pack(fill="both", expand=True)

        # Colores de estado
        self.tree_det.tag_configure("listo", background="#1e4620", foreground="white")
        self.tree_det.tag_configure("arreglar", background="#3e3e0e", foreground="white")
        self.tree_det.tag_configure("meta", background="#2b2b2b", foreground="#bfbfbf")

        # Filas alternadas
        self.tree_det.tag_configure("oddrow", background="#1e1e1e")
        self.tree_det.tag_configure("evenrow", background="#2b2b2b")

        self.tree_det.bind("<Double-1>", self.on_double_click_detalle)

    # --- POPUP PARA CLIENTES ---
    def abrir_popup_cliente(self):
        popup = ttk.Toplevel(self.root)
        popup.title("Agregar Cliente")
        popup.geometry("350x180")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        ttk.Label(popup, text="Nombre del Cliente:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(20, 5))
        entry_nombre = ttk.Entry(popup, width=35)
        entry_nombre.pack(padx=15, pady=(0, 15))

        def guardar_cliente():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "Debe ingresar un nombre.")
                return
            try:
                Cliente.agregar(nombre)
                messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente.")
                popup.destroy()
                self.cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente:\n{e}")

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Guardar", command=guardar_cliente, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=popup.destroy, bootstyle="secondary").pack(side="left", padx=5)

    # --- FUNCIONES DE DATOS ---
    def cargar_clientes(self):
        clientes = Cliente.obtener_todos(self.var_buscar.get().strip())
        self.tree_clientes.delete(*self.tree_clientes.get_children())

        for i, c in enumerate(clientes):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_clientes.insert("", "end", iid=c["Id"], values=(c["nombre"], c["cantidad"] or 0), tags=(tag,))

        self.tree_det.delete(*self.tree_det.get_children())

    def on_cliente_select(self, _):
        sel = self.tree_clientes.selection()
        if sel:
            self.mostrar_detalles_cliente(sel[0])

    def mostrar_detalles_cliente(self, id_cliente):
        artefactos = Artefacto.obtener_por_cliente(id_cliente)
        self.tree_det.delete(*self.tree_det.get_children())
        if not artefactos:
            self.tree_det.insert("", "end", values=("", "", "", "Este cliente no tiene artefactos o arreglos."), tags=("meta",))
            return
        for i, art in enumerate(artefactos):
            tag_estado = "listo" if (art["estado"] or "").lower() == "listo" else "arreglar"
            tag_fila = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_det.insert("", "end", iid=f"art_{art['Id']}",
                     values=(art["estado"], art["fecha"], art["detalle"]),
                     tags=(tag_estado, tag_fila))

    def on_double_click_detalle(self, _):
       sel = self.tree_det.selection()
       if not sel:
        return

       iid = sel[0]
       if not iid.startswith("art_"):
        return

       id_artefacto = iid.split("_")[1]

       artefacto = Artefacto.obtener_por_id(id_artefacto)
       if not artefacto:
        return

       estado_actual = (artefacto["estado"] or "").lower()
       nuevo_estado = "Listo" if estado_actual != "listo" else "Arreglar"

       Artefacto.cambiar_estado(id_artefacto, nuevo_estado)
       self.mostrar_detalles_cliente(self.tree_clientes.selection()[0])


    def abrir_popup_arreglo(self):
        sel_cliente = self.tree_clientes.selection()
        if not sel_cliente:
            messagebox.showwarning("Atención", "Seleccione un cliente para agregar un arreglo.")
            return
        abrir_agregar_arreglo(self.root, sel_cliente[0], self.refrescar_cliente, self.cargar_clientes)

    def refrescar_cliente(self):
        sel = self.tree_clientes.selection()
        if sel:
            self.mostrar_detalles_cliente(sel[0])

    def eliminar_arreglo(self):
        sel = self.tree_det.selection()
        if not sel:
            return
        iid = sel[0]
        if not iid.startswith("art_"):
            return
        id_artefacto = iid.split("_")[1]
        if not messagebox.askyesno("Confirmar", "¿Eliminar este arreglo y su artefacto asociado?"):
            return
        Artefacto.eliminar(id_artefacto)
        self.refrescar_cliente()
        self.cargar_clientes()

    def eliminar_cliente(self):
        sel = self.tree_clientes.selection()
        if not sel:
            return
        id_cliente = sel[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar este cliente y todos sus arreglos y artefactos?"):
            return
        Cliente.eliminar(id_cliente)
        self.cargar_clientes()
        self.tree_det.delete(*self.tree_det.get_children())
