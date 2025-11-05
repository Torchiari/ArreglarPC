from database.queries import GET_CLIENTES, INSERT_CLIENTE, DELETE_CLIENTE
from database.connection import get_connection

class Cliente:
    @staticmethod
    def obtener_todos(nombre_filtro=None):
        conn, cursor = get_connection()
        filtro = ""
        params = ()
        if nombre_filtro:
            filtro = "WHERE c.nombre LIKE %s"
            params = (f"%{nombre_filtro}%",)
        cursor.execute(GET_CLIENTES.format(filtro=filtro), params)
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def agregar(nombre):
        conn, cursor = get_connection()
        cursor.execute(INSERT_CLIENTE, (nombre,))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_cliente):
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM artefacto WHERE Id IN (SELECT `id.artefacto` FROM arreglo WHERE `id.cliente`=%s)", (id_cliente,))
        cursor.execute("DELETE FROM arreglo WHERE `id.cliente`=%s", (id_cliente,))
        cursor.execute(DELETE_CLIENTE, (id_cliente,))
        conn.commit()
        conn.close()
