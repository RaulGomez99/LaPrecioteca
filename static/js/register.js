const url = "http://127.0.0.1:8000/"
window.onload = () => {
    document.getElementById("register_btn").addEventListener("click", register)
}

async function register(){
    console.log("Registrar")

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    console.log(csrftoken)
    const name = document.getElementById("name").value
    const surname = document.getElementById("surname").value
    const email = document.getElementById("email").value
    const tlf = document.getElementById("tlf").value
    const username = document.getElementById("username").value
    const password1 = document.getElementById("password1").value
    const password2 = document.getElementById("password2").value

    let error = ""
    if(name == "") error += "Falta escribir el nombre.\n"
    if(surname == "") error += "Falta escribir los apellidos.\n"
    if(email == "") error += "Falta escribir el email.\n"
    if(tlf == "") error += "Falta escribir el telefono.\n"
    if(username == "") error += "Falta escribir el nombre de usuario.\n"
    if(password1 == "") error += "Falta escribir el password.\n"
    if(password2 == "") error += "Falta repetir el password.\n"

    if(password1 != password2) error += "Los passwords deben ser iguales.\n"

    if(error != ""){
        alert("Errores:\n" + error)
        return
    }

    const json = {
        name, surname, email, tlf, username, password1, password2
    }

    const req = await fetch("/register_user", {
        method: "POST", 
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    const json2 = await req.json()
    if(json2.error) alert(json2.error)
    else window.location.pathname = "/"

}