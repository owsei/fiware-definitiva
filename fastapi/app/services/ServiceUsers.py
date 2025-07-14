import dbQuerys
import bcrypt
from fastapi import HTTPException

def user_exists(usuario: str):
    """
    Verifica si un usuario ya existe en la base de datos.
    """
    query = "SELECT idUsuario FROM usuarios WHERE nombre = %s"
    values = (usuario,)
    print(f"Query de verificación de usuario: {query}")
    
    try:
        user = dbQuerys.selectOne(query, values)
        if user is None:
            return False
        
        if "error" in user:
            return {"message": "Error al verificar el usuario", "error": user["error"]}
        
        if user:
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error al verificar el usuario: {e}")
        return {"message": "ErrorException: al verificar el usuario","operacion":"501","error":{e}}
    
def validate_user_token(token: str):
    """
    Valida el token de un usuario.
    """
    query = "SELECT idUsuario, nombre, password, token FROM usuarios WHERE token = '" + token + "'"
    print(f"Query de validación de token: {query}")
    
    try:
        user = dbQuerys.selectOne(query)
        if user is None:
            return {"message": "Token no válido","error": 403 }
        
        if "error" in user:
            return {"message": "Error al validar el token", "error": user["error"]}
        
        return {"message": "✅ Token válido","user":user}
    
    except Exception as e:
        print(f"Error al validar el token: {e}")
        return {"message": "ErrorException: al validar el token","operacion":"501","error":{e}}

def validate_user(usuario: str, password: str):
    """
    Valida si el usuario y la contraseña son correctos.
    """
    query = "SELECT idUsuario, nombre, password, token FROM usuarios WHERE nombre = %s"
    values = (usuario,)
    print(f"Query de validación: {query}")
    
    try:
        user = dbQuerys.selectOne(query, values)
        if user is None:
            return {"message": "Usuario No existe","error": 404 }
        
        if "error" in user:
            return {"message": "Error al validar el usuario", "error": user["error"]}
        
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                return {"message": "✅ Login exitoso","user":user}
            else:
                return {"message": "✅ Login exitoso","error": "Usuario o contraseña incorrectos"}
        else:
            return {"error": "Usuario o contraseña incorrectos"}
    
    except Exception as e:
        print(f"Error al validar el usuario: {e}")
        return {"message": "ErrorException: al validar el usuario","operacion":"501","error":{e}}

def register_user(usuario: str, password: str):
    """
    Crea un nuevo usuario en la base de datos.
    """
    query= "Insert into usuarios (nombre, password, deshabilitado) values (%s,%s,%s) RETURNING idUsuario;"
    values = (usuario, password.decode('utf-8'), False)
    print(f"Query de registro: {query}")
    try:
        print(f"Valores a insertar: {password}, {usuario}")
        nuevo_usuario = dbQuerys.insert(query,values)
        if "error" in nuevo_usuario:
            return {"message": "Error al crear el usuario", "error": nuevo_usuario["error"]}
        
        id =nuevo_usuario.get("id")
        print(f"Nuevo usuario INSERTADO: {id}")
        return {"message": "Insertado correctamente", "id": id}
    
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        return {"message": "ErrorException: al crear el usuario ","operacion":"501","error":{e}}
    
def updateUserToken(idUsuario: str, token: str):
    """
    Actualiza el token de un usuario en la base de datos.
    """
    query = f"UPDATE usuarios SET token = %s WHERE idUsuario = %s ;"
    values = (token,idUsuario)
    try:
        dbQuerys.update(query, values)
        return {"message": "Token actualizado correctamente"}
    except Exception as e:
        print(f"Error al actualizar el token: {e}")
        return {"message": "Error al actualizar el token", "error": str(e)}

def logout(usuario: str):
    """
    Elimina el token de un usuario en la base de datos.
    """
    query = "UPDATE usuarios SET token = NULL WHERE idUsuario = %s;"
    values = (usuario,)
    try:
        dbQuerys.update(query, values)
        return {"message": "Token eliminado correctamente"}
    except Exception as e:
        print(f"Error al eliminar el token: {e}")
        return {"message": "Error al eliminar el token", "error": str(e)}