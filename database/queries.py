GET_CLIENTES = """
    SELECT c.Id, c.nombre, COUNT(a.`id.artefacto`) AS cantidad
    FROM cliente c
    LEFT JOIN arreglo a ON c.Id = a.`id.cliente`
    {filtro}
    GROUP BY c.Id, c.nombre
    ORDER BY c.nombre ASC
"""

GET_ARTEFACTOS_BY_CLIENTE = """
    SELECT * FROM artefacto 
    WHERE Id IN (SELECT `id.artefacto` FROM arreglo WHERE `id.cliente`=%s)
    ORDER BY Id ASC
"""

INSERT_CLIENTE = "INSERT INTO cliente (nombre) VALUES (%s)"
DELETE_CLIENTE = "DELETE FROM cliente WHERE Id=%s"

INSERT_ARTEFACTO = "INSERT INTO artefacto (estado, fecha, detalle) VALUES (%s,%s,%s)"
INSERT_ARREGLO = "INSERT INTO arreglo (`id.cliente`,`id.artefacto`) VALUES (%s,%s)"

DELETE_ARREGLO = "DELETE FROM arreglo WHERE `id.artefacto`=%s"
DELETE_ARTEFACTO = "DELETE FROM artefacto WHERE Id=%s"

UPDATE_ESTADO_ARTEFACTO = "UPDATE artefacto SET estado=%s WHERE Id=%s"
GET_ESTADO_ARTEFACTO = "SELECT estado FROM artefacto WHERE Id=%s"
