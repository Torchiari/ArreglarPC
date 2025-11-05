from database.queries import GET_ARTEFACTOS_BY_CLIENTE, UPDATE_ESTADO_ARTEFACTO, INSERT_ARTEFACTO, INSERT_ARREGLO, DELETE_ARREGLO, DELETE_ARTEFACTO
from database.connection import get_connection

class Artefacto:
    @staticmethod
    def obtener_por_cliente(id_cliente):
        conn, cursor = get_connection()
        cursor.execute(GET_ARTEFACTOS_BY_CLIENTE, (id_cliente,))
        data = cursor.fetchall()
        conn.close()
        return data
    @staticmethod
    def obtener_por_id(id_artefacto):
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM artefacto WHERE Id = %s", (id_artefacto,))
        data = cursor.fetchone()
        conn.close()
        return data

    @staticmethod
    def cambiar_estado(id_artefacto, nuevo_estado):
        conn, cursor = get_connection()
        cursor.execute(UPDATE_ESTADO_ARTEFACTO, (nuevo_estado, id_artefacto))
        conn.commit()
        conn.close()

    @staticmethod
    def crear(estado, fecha, detalle, id_cliente):
        conn, cursor = get_connection()
        cursor.execute(INSERT_ARTEFACTO, (estado, fecha, detalle))
        id_artefacto = cursor.lastrowid
        cursor.execute(INSERT_ARREGLO, (id_cliente, id_artefacto))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_artefacto):
        conn, cursor = get_connection()
        cursor.execute(DELETE_ARREGLO, (id_artefacto,))
        cursor.execute(DELETE_ARTEFACTO, (id_artefacto,))
        conn.commit()
        conn.close()
