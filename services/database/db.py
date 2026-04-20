import dotenv
import os
import pymysql
from pymysql import Error

dotenv.load_dotenv()

# Obtener las variables de entorno para la conexión a la base de datos
DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def database_connection():
    try:
        # Establecer la conexión con los parámetros requeridos
        conexion = pymysql.connect(
            host=DB_ENDPOINT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if conexion.open:
            print('Conexión exitosa a la base de datos.')
            return conexion

    except Error as error:
        print(f'Error al conectar a MySQL: {error}')

def get_boletin(boletin_id, email):
    try:
        conexion = database_connection()
        cursor = conexion.cursor()

        # Consulta para obtener el boletín por ID y email
        get_boletin_query = '''
        SELECT boletin_id, message, email, link_s3, flag
        FROM boletines
        WHERE boletin_id = %s AND email = %s
        '''
        cursor.execute(get_boletin_query, (boletin_id, email))
        result = cursor.fetchone()

        if result:
            boletin_data = {
                'boletin_id': result[0],
                'message': result[1],
                'email': result[2],
                'link_s3': result[3],
                'flag': result[4]
            }
            return boletin_data
        else:
            print('No se encontró el boletín con el ID y email proporcionados.')
            return None

    except Error as error:
        print(f'Error al obtener el boletín: {error}')
    finally:
        if 'conexion' in locals() and conexion.open:
            cursor.close()
            conexion.close()
            print('Conexión a la base de datos cerrada.')
    return None

def mark_as_read(boletin_id):
    try:
        conexion = database_connection()
        cursor = conexion.cursor()

        # Consulta para marcar el boletín como leído
        mark_as_read_query = '''
        UPDATE boletines
        SET flag = TRUE
        WHERE boletin_id = %s
        '''
        cursor.execute(mark_as_read_query, (boletin_id,))
        conexion.commit()
        print(f'Boletín con ID {boletin_id} marcado como leído.')

    except Error as error:
        print(f'Error al marcar el boletín como leído: {error}')
    finally:
        if 'conexion' in locals() and conexion.open:
            cursor.close()
            conexion.close()
            print('Conexión a la base de datos cerrada.')