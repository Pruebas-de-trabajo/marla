import os
import pandas as pd
import mysql.connector

from tabulate import tabulate
from dotenv import load_dotenv
from mysql.connector import Error
from openai import OpenAI

load_dotenv('.env')

HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TABLE_NAME = os.getenv('TABLE_NAME')
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)


def get_and_download_data():
    global connection
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = connection.cursor()

            # Consultar y obtener todos los datos
            query = f"SELECT * FROM {TABLE_NAME}"
            cursor.execute(query)

            column_names = [column[0] for column in cursor.description]
            records = cursor.fetchall()

            # Pasar datos a un DataFrame para análisis
            df = pd.DataFrame.from_records(records, columns=column_names)

            # Exportar a csv para no hacer tantas consultas a la BD.
            df.to_csv("data.csv", index=False, mode='w')
            print(f"Datos exportados a data.csv ({len(df)} registros)")

            # Cerrar conexión
            cursor.close()
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión cerrada")


def calculate_sng(satisfaction, dissatisfaction, total_records):
    try:
        return round((satisfaction * 100) / total_records) - round((dissatisfaction * 100) / total_records)
    except Exception as e:
        print(e)
        return 0


def call_chat_gpt(data, key_word):
    messages = []
    for comment in data:
        prompt = f"Analiza el siguiente texto y determina si es positivo, negativo o neutral:\n\nTexto: '{comment}'"
        prompt2 = f"Analiza el siguiente texto y determina los problemas del usuario y sus conclusiones:\n\nTexto: '{comment}'"

        if key_word == 'feelings':
            messages.append({'role': 'user', 'content': prompt})
        else:
            messages.append({'role': 'user', 'content': prompt2})

        # Solicitar una respuesta a GPT-3
        completion = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
        )
        assistant_response = completion.choices[0].message.content
        print(assistant_response)


def see_stats():
    df = pd.read_csv('data.csv')

    # Configurar tipos para cada columna
    str_columns = ['email', 'conocia_empresa']
    int_columns = ['satisfeccion_general', 'recomendacion']
    df[str_columns] = df[str_columns].astype(str)
    df[int_columns] = df[int_columns].astype(int)
    df['fecha'] = pd.to_datetime(df['fecha'])

    total_records = df.shape[0]
    # (1 - a) SNG de la pregunta (campo: "satisfeccion_general").
    general_satisfaction = df['satisfeccion_general'].between(6, 7).sum()
    general_dissatisfaction = df['satisfeccion_general'].between(1, 4).sum()
    sng_satisfaction = calculate_sng(general_satisfaction, general_dissatisfaction, total_records)

    # (1 - b) Total de personas que respondieron que conocían a la empresa.
    people_known_company = df[df['conocia_empresa'] == 'Sí'].shape[0]

    # (1 - c) SNG de la recomendación. (campo: "recomendacion")
    rec_satisfaction = df['recomendacion'].between(6, 7).sum()
    rec_dissatisfaction = df['recomendacion'].between(1, 4).sum()
    sng_recommendation = calculate_sng(rec_satisfaction, rec_dissatisfaction, total_records)

    # (1 - d) Nota promedio de la recomendación. (campo: "recomendacion")
    average_recommendation = df['recomendacion'].mean()

    # (1 - e) Total de personas que hicieron un comentario.
    people_comments = df['recomendacion_abierta'].dropna().count()

    # (1 - f) Días, meses que llevo la encuesta.
    first_survey = df['fecha'].min()
    last_survey = df['fecha'].max()

    days = (last_survey - first_survey).days
    months = days // 30

    data = [
        ["SNG Satisfacción general", sng_satisfaction],
        ["Total personas que conocían la empresa", people_known_company],
        ["SNG Recomendación", sng_recommendation],
        ["Nota promedio recomendación", average_recommendation],
        ["Total Comentarios", people_comments],
        ["Total tiempo (días, meses)", f"{days} días, ({months} meses y {days % 30} días)"]
    ]

    # (2 - a) Análisis de sentimiento por persona que dio una respuesta abierta.
    call_chat_gpt(df['recomendacion_abierta'].dropna(), 'feelings')

    # (2 - b) Problemas principales y conclusión.
    call_chat_gpt(df['recomendacion_abierta'].dropna(), 'problems')

    print(tabulate(data, headers=["Descripción", "Valor"], tablefmt="grid"))


def main_menu():
    print("Bienvenido, ¿Qué desea hacer?")
    print("1. Obtener y descargar los datos")
    print("2. Ver reporte de los datos")
    print("3. Salir")
    print()


while True:
    main_menu()
    choice = input("Escriba un número (1-4): ")

    if choice == '1':
        get_and_download_data()
    if choice == '2':
        see_stats()
    elif choice == '3':
        print("Eligió salir del programa. ¡Adiós!")
        break
    else:
        print("Opción inválida. Por favor intente de nuevo")

    input("\nPresione Enter para continuar...")

if __name__ == '__main__':
    main_menu()

