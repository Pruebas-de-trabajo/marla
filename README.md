# Proyecto Marla - Análisis de Satisfacción y Recomendaciones

Este repositorio contiene el código y los resultados del análisis de satisfacción y recomendaciones para el proyecto
Marla de MK desarrollador inmobiliario.

## Descripción del Proyecto

MK desarrollador inmobiliario enfrenta problemas de satisfacción del cliente con respecto al proyecto Marla. Este
repositorio contiene el código necesario para analizar los datos de una encuesta realizada a los clientes, así como los
resultados obtenidos y el informe generado.

## Estructura del Repositorio

- **prueba.py**: Archivo principal que contiene el código Python para analizar los datos de la encuesta.
- **requirements.txt**: Dependencias necesarias para que el proyecto funcione correctamente.
- **.gitignore**: Archivo para ignorar archivos sencibles.
- **data.csv**: Archivo que contiene los datos para el análisis. (se genera dinámicamente)
- **README.md**: Este archivo, proporcionando una guía rápida sobre el proyecto.

## Requisitos de Software

[![Python][python-badge]][python-url]

## Instrucciones de Uso

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/Pruebas-de-trabajo/marla.git
   cd marla 
   ```
   
2. **Crear entorno virtual (opcional, recomendado):**

- Con la librería virtualenv, crea un entorno virtual llamado 
**venv** en la raíz del proyecto.
    ```bash
   virtualenv venv --python=python3.11.9
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**

- Crear un archivo **.env** en la raíz del proyecto.
   ```bash
   HOST=
   DATABASE=
   USER=
   PASSWORD=
   TABLE_NAME=
   OPENAI_API_KEY=
   ```

5. **Ejecutar Script:**
   ```bash
   python prueba.py
   ```

[python-badge]: https://img.shields.io/badge/Python-3.11.9-ffffff?style=for-the-badge&logo=python&logoColor=ffff00

[python-url]: https://python.org/