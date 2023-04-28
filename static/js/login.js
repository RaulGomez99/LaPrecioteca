const url = "http://127.0.0.1:8000/"
window.onload = () => {
    document.getElementById("login_btn").addEventListener("click", login)
    document.getElementById("password1").addEventListener("keydown", (ev) => {
        console.log(ev.key)
        if(ev.key == "Enter") login()
    })
}

async function login(){
    console.log("Login")

    const csrftoken = getCookie('csrftoken')
    console.log(csrftoken)
    console.log("Nuevo")
    const username = document.getElementById("username").value
    const password1 = document.getElementById("password1").value

    let error = ""

    if(username == "") error += "Falta escribir el nombre de usuario.\n"
    if(password1 == "") error += "Falta escribir el password.\n"

    if(error != ""){
        alert("Errores:\n" + error)
        return
    }

    const json = {
        username, password1
    }

    console.log(json)

    const req = await fetch("/login_user", {
        method: "POST", 
        
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(json)
    })
    const json2 = await req.json()
    if(json2.error) alert(json2.error)
    else window.location.pathname = "/"

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}