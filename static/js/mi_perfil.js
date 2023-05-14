window.onload = () => {
    document.getElementById("edit").addEventListener("click", edit)
}

async function edit(){
    const csrftoken = getCookie('csrftoken')
    const name = document.getElementById("nombre").value
    const surname = document.getElementById("apellidos").value
    const email = document.getElementById("email").value
    const tlf = document.getElementById("phone").value
    const password = document.getElementById("contrasena").value

    let error = ""
    if(name == "") error += "Falta escribir el nombre.\n"
    if(surname == "") error += "Falta escribir los apellidos.\n"
    if(email == "") error += "Falta escribir el email.\n"
    if(tlf == "") error += "Falta escribir el telefono.\n"
    
    if(error != ""){
        alert("Errores:\n" + error)
        return
    }

    const json = {
        name, surname, email, tlf, password
    }

    const req = await fetch("/edit_user/", {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    const json2 = await req.json()
    console.log(json2)
    if(json2.error) alert(json2.error)
    else alert("Cambios guardados correctamente")

}