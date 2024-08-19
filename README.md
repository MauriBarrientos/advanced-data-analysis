# Ejercicio de Repaso Librerías Python

Una vez clonado el repositorio, crear un entorno virtual y acceder al mismo:
```bash
virtualenv venv
```
```bash
source venv/Scripts/activate
```
Instalar las dependencias:
```bash
pip install -r requirements.txt
```

En el archivo `main.py`, cambiar las credenciales de la linea `6` en caso de ser necesario
```python
user = "root"
password = ""
host = "localhost"
```

Para probar cada uno de los ejercicios, en la ultima linea escribir un `print()` dentro del cuál invocar la función correspondiente

```python
print(total_employees_per_department()) # Ejemplo
```