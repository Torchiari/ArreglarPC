from database.connection import get_connection
from database.queries import INSERT_BOLETA, GET_BOLETAS_BY_CLIENTE, GET_BOLETA_BY_ARTEFACTO

class Boleta:
    @staticmethod
    def crear(fecha, valor, detalle, id_cliente, id_artefacto):
        conn, cursor = get_connection()
        cursor.execute(INSERT_BOLETA, (fecha, valor, detalle, id_cliente, id_artefacto))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_cliente(id_cliente):
        conn, cursor = get_connection()
        cursor.execute(GET_BOLETAS_BY_CLIENTE, (id_cliente,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def obtener_por_artefacto(id_artefacto):
        conn, cursor = get_connection()
        cursor.execute(GET_BOLETA_BY_ARTEFACTO, (id_artefacto,))
        data = cursor.fetchone()
        conn.close()
        return data
