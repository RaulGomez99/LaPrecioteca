const url = "http://127.0.0.1:8000/"
window.onload = function () {
    const products = document.querySelectorAll(".product")
    products.forEach(product => {
        product.addEventListener("click", createPopUpComplete)
    });
}

async function createPopUpComplete(ev) {
    ev.preventDefault()
    const product = ev.currentTarget
    const resp = await fetch("/product/" + product.id)
    const json = await resp.json()
    createPopUp(json)
}

function createPopUp(product) {
    console.log(product)
    const divPopUp = document.createElement("div")
    divPopUp.classList.add("popup")

    const backgroundPopUp = document.createElement("div")
    backgroundPopUp.addEventListener("click", removePopUp)
    backgroundPopUp.classList.add("background_popup")

    const crossMark = document.createElement("span")
    crossMark.classList.add("cross_mark")
    crossMark.innerText = "X"
    crossMark.addEventListener("click", removePopUp)

    const titleProduct = document.createElement("div")
    titleProduct.classList.add("title_product")
    titleProduct.innerHTML = `<strong>${product.name}</strong>`

    const imageProductDiv = document.createElement("div")
    imageProductDiv.classList.add("image_product_popup")
    const imageProduct = document.createElement("img")
    imageProduct.src = product.photo

    const infoProduct = document.createElement("div")
    infoProduct.classList.add("info_product_popup")
    infoProduct.innerHTML = "<span>Descripción:</span>"
    const descProduct = document.createElement("div")
    descProduct.classList.add("desc_product_popup")
    descProduct.innerText = product.description

    const divMoreInfo = document.createElement("a")
    divMoreInfo.classList.add("more_info_popup")
    divMoreInfo.innerText = "Ver más información"
    divMoreInfo.href = url + "product_info/" + product.id
    divMoreInfo.target = "blank"

    const div_carro = document.createElement("div")
    div_carro.style.display = "inline"
    const imgCarro = document.createElement("img")
    imgCarro.classList.add("carrito")
    if (product.is_favourite) imgCarro.classList.add("fav")
    imgCarro.addEventListener("click", async () => {
        const resp = await fetch("/toggle_fav/" + product.id)
        const json = await resp.json()
        console.log(json)
        if (json.ok) imgCarro.classList.toggle("fav")
        else alert(json.error)
    })
    imgCarro.src = "/static/media/carro.png"
    div_carro.appendChild(imgCarro)

    divPopUp.appendChild(crossMark)
    divPopUp.appendChild(titleProduct)
    imageProductDiv.appendChild(imageProduct)
    divPopUp.appendChild(imageProductDiv)
    infoProduct.appendChild(descProduct)
    divPopUp.appendChild(infoProduct)
    divPopUp.appendChild(document.createElement("br"))
    divPopUp.appendChild(divMoreInfo)
    divPopUp.appendChild(div_carro)

    const insert = document.getElementById("insert_popup")
    insert.appendChild(divPopUp)
    insert.appendChild(backgroundPopUp)
    const body = document.getElementsByTagName("body")[0]
    body.style.overflow = "hidden"
}

function removePopUp() {
    const insert = document.getElementById("insert_popup")
    insert.innerHTML = ""
    const body = document.getElementsByTagName("body")[0]
    body.style.overflow = "auto"
}