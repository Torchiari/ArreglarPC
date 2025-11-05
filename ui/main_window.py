import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from models.cliente import Cliente
from models.artefacto import Artefacto
from ui.cliente_popup import abrir_agregar_cliente
from ui.arreglo_popup import abrir_agregar_arreglo

class ArregloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💻 Programa Danel")
        self.root.geometry("1200x680")
        self.style = ttk.Style("flatly")

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        frame_top = ttk.Frame(self.root, padding=(20,15))
        frame_top.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_top, text="🔍 Buscar cliente:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.var_buscar = ttk.StringVar()
        entry_buscar = ttk.Entry(frame_top, textvariable=self.var_buscar, width=35, bootstyle="info")
        entry_buscar.pack(side="left", padx=5)
        entry_buscar.bind("<Return>", lambda e: self.cargar_clientes())

        ttk.Button(frame_top, text="Buscar", command=self.cargar_clientes, bootstyle="primary").pack(side="left", padx=5)

        top_right = ttk.Frame(frame_top)
        top_right.pack(side="right")
        ttk.Button(top_right, text="🔄 Refrescar", command=self.cargar_clientes, bootstyle="secondary-outline").pack(side="left", padx=5)
        ttk.Button(top_right, text="➕ Nuevo Arreglo", command=self.abrir_popup_arreglo, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(top_right, text="🗑️ Eliminar Arreglo", command=self.eliminar_arreglo, bootstyle="danger").pack(side="left", padx=5)

        panel = ttk.Frame(self.root, padding=10)
        panel.pack(fill="both", expand=True)

        # Panel clientes
        frame_izq = ttk.Frame(panel, bootstyle="secondary", padding=15)
        frame_izq.pack(side="left", fill="y", padx=(0, 15))

        ttk.Label(frame_izq, text="👤 Clientes", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Button(frame_izq, text="➕ Agregar", command=lambda: abrir_agregar_cliente(self.root, self.cargar_clientes), bootstyle="success-outline").pack(anchor="w", pady=4)
        ttk.Button(frame_izq, text="🗑️ Eliminar", command=self.eliminar_cliente, bootstyle="danger-outline").pack(anchor="w", pady=4)

        columnas_clientes = ("nombre", "artefactos")
        self.tree_clientes = ttk.Treeview(frame_izq, columns=columnas_clientes, show="headings", height=25)
        self.tree_clientes.heading("nombre", text="Nombre y Apellido")
        self.tree_clientes.heading("artefactos", text="N° de Artefactos")
        self.tree_clientes.pack(fill="y", expand=True, pady=5)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.on_cliente_select)

        # Panel artefactos
        frame_der = ttk.Frame(panel, bootstyle="secondary", padding=15)
        frame_der.pack(side="right", fill="both", expand=True)

        ttk.Label(frame_der, text="🔧 Artefactos y Arreglos", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        columnas = ("tipo", "estado", "fecha", "detalle")
        self.tree_det = ttk.Treeview(frame_der, columns=columnas, show="headings", height=25)
        for col in columnas:
            self.tree_det.heading(col, text=col.capitalize())
        self.tree_det.pack(fill="both", expand=True, pady=5)
        self.tree_det.tag_configure("listo", background="#d4edda")
        self.tree_det.tag_configure("arreglar", background="#fff3cd")
        self.tree_det.tag_configure("meta", background="#e2e3e5")
        self.tree_det.bind("<Double-1>", self.on_double_click_detalle)

    def cargar_clientes(self):
        clientes = Cliente.obtener_todos(self.var_buscar.get().strip())
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for c in clientes:
            self.tree_clientes.insert("", "end", iid=c["Id"], values=(c["nombre"], c["cantidad"] or 0))
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
        for art in artefactos:
            tag = "listo" if (art["estado"] or "").lower() == "listo" else "arreglar"
            self.tree_det.insert("", "end", iid=f"art_{art['Id']}",
                                 values=("Artefacto", art["estado"], art["fecha"], art["detalle"]),
                                 tags=(tag,))

    def on_double_click_detalle(self, _):
        sel = self.tree_det.selection()
        if not sel: return
        iid = sel[0]
        if not iid.startswith("art_"): return
        id_artefacto = iid.split("_")[1]
        artefactos = Artefacto.obtener_por_cliente(id_artefacto)
        nuevo = "Listo" if (artefactos[0]["estado"] or "").lower() != "listo" else "Arreglar"
        Artefacto.cambiar_estado(id_artefacto, nuevo)
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
        if not sel: return
        iid = sel[0]
        if not iid.startswith("art_"): return
        id_artefacto = iid.split("_")[1]
        if not messagebox.askyesno("Confirmar", "¿Eliminar este arreglo y su artefacto asociado?"):
            return
        Artefacto.eliminar(id_artefacto)
        self.refrescar_cliente()
        self.cargar_clientes()

    def eliminar_cliente(self):
        sel = self.tree_clientes.selection()
        if not sel: return
        id_cliente = sel[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar este cliente y todos sus arreglos y artefactos?"):
            return
        Cliente.eliminar(id_cliente)
        self.cargar_clientes()
        self.tree_det.delete(*self.tree_det.get_children())
