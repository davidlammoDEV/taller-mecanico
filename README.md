# 🚗 Taller Mecánico - API

Sistema de gestión para taller mecánico desarrollado con **FastAPI** y **PostgreSQL**.

---

## 📋 Requisitos previos

- Python 3.10 o superior
- PostgreSQL
- Git

---
## Antes de la instalación recordar
```
Importar la nueva bd llamada respaldo.sql y actulizar requirements.txt 
```

## 🚀 Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/davidlammoDEV/taller-mecanico.git
```

### 2. Crear y activar entorno virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
#### En el Query Tool de PgAdmin coloca:

```bash
CREATE DATABASE taller;

-- Opcional
CREATE USER postgres WITH PASSWORD '3690';
ALTER USER postgres WITH SUPERUSER;
```
#### Nota: El proyecto actualmente usa la conexión
```bash
postgresql://postgres:3690@localhost:5432/taller
```
Si quieres cambiar la contraseña o el nombre de la BD, edita el archivo database/connection.py. es recomendable usar una base de datos vacia antes de ejecutar el programa

### 5. Iniciar el servidor

```bash
uvicorn main:app --reload
```
