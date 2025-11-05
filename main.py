import ttkbootstrap as ttk
from ui.main_window import ArregloApp

if __name__ == "__main__":
    root = ttk.Window()
    app = ArregloApp(root)
    root.mainloop()
