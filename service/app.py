from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de conexión a MySQL
db_config = {
    "host": "mysql-service",  # nombre del pod de MySQL en Kubernetes
    "user": "testuser",
    "password": "testpass",
    "database": "testdb"
}

def get_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Crear un cliente
@app.route("/clientes", methods=["POST"])
def create_cliente():
    data = request.json
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO cliente (nombre, correo, telefono) VALUES (%s, %s, %s)",
                   (data["nombre"], data["correo"], data.get("telefono")))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Cliente creado"}), 201

# Obtener todos los clientes
@app.route("/clientes", methods=["GET"])
def get_clientes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(results)

# Obtener un cliente por ID
@app.route("/clientes/<int:id>", methods=["GET"])
def get_cliente(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "Cliente no encontrado"}), 404

# Actualizar cliente
@app.route("/clientes/<int:id>", methods=["PUT"])
def update_cliente(id):
    data = request.json
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE cliente SET nombre=%s, correo=%s, telefono=%s WHERE id=%s",
                   (data["nombre"], data["correo"], data.get("telefono"), id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Cliente actualizado"})

# Eliminar cliente
@app.route("/clientes/<int:id>", methods=["DELETE"])
def delete_cliente(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM cliente WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Cliente eliminado"})

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
