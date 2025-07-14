const urlBase = "http://127.0.0.1:8000";


function usuarioLogeado() {

    let item = window.localStorage.getItem("userCesiumData")
    if (item) {
      const userData = JSON.parse(item);
      if (!userData && userData.token =='') {
        window.location.href = "index.html"; // Redirige a la página de inicio de sesión si el token está vacío
      }
      else {
        // Si el token existe, puedes usarlo para realizar solicitudes autenticadas
        console.log("Token de usuario:", userData.token);
        window.token = userData.token; // Guarda el token en una variable global
        window.userId = userData.idusuario; // Guarda el ID del usuario en una variable global
      } 
      
      console.log("Datos del usuario:", userData);
    } else {
      window.location.href = "index.html"; // Redirige a la página de inicio de sesión si el token está vacío
    }

}


function login() {

    const usuarioT = document.getElementById("username").value;
    const passwordT = document.getElementById("password").value; 

    if (!usuarioT || !passwordT) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    urlLogin= urlBase + '/login';
    // Realiza una solicitud POST al servidor FastAPI para iniciar sesión
    fetch(urlLogin, {
        method: 'POST', // Método HTTP
        headers: {
            'Content-Type': 'application/json' // Tipo de contenido
        },
        body: JSON.stringify({ usuario: usuarioT,password:passwordT }) // Datos del formulario
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.message + " " + data.error);
            } else {
                // Redirigir al usuario a la página de inicio después de un inicio de sesión exitoso
                window.localStorage.setItem("userCesiumData", JSON.stringify(data));
                window.location.href = "principal.html"; // Cambia a la URL de tu página de inicio
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo.");
        });
}