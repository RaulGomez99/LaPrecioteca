let products
window.onload = () => {
    products = Array.from(document.querySelectorAll(".my-data")).map(product => (
        JSON.parse(product.getAttribute("data-my-data").replace(/'/g, '"'))
    ))
    document.getElementById("lupa").addEventListener("click", filter)
    document.querySelectorAll(".filter_super").forEach(supermarket => supermarket.addEventListener("click", cambiarSuper))
    render(products)
}


function render(products) {
    const productZone = document.getElementById("product_zone")
    productZone.innerHTML = ""
    products.forEach(product => {
        const productDiv = document.createElement("div")
        productDiv.classList.add("product")
        productDiv.id = product.id
        const logoSuper = document.createElement("img")
        logoSuper.src = product.supermarket.url_logo
        logoSuper.classList.add("logo")
        productDiv.appendChild(logoSuper)
        const imageDiv = document.createElement("div")
        imageDiv.classList.add("image_div")
        const imgDiv = document.createElement("img")
        imgDiv.classList.add("image")
        imgDiv.src = product.product_photo
        imgDiv.loading = "lazy"
        imageDiv.appendChild(imgDiv)
        productDiv.appendChild(imageDiv)
        const textDiv = document.createElement("div")
        textDiv.classList.add("text")
        textDiv.innerHTML = `<strong>${product.name}</strong>${product.price}€`
        productDiv.appendChild(textDiv)
        productZone.appendChild(productDiv)
        productDiv.addEventListener("click", createPopUpComplete)
    });
}

function cambiarSuper(ev) {
    ev.preventDefault()
    const supermarket = ev.currentTarget
    if (supermarket.classList.contains("filter_super")) {
        supermarket.classList.remove("filter_super")
        supermarket.classList.add("no_filter")
    } else {
        supermarket.classList.remove("no_filter")
        supermarket.classList.add("filter_super")
    }
}

function filter() {
    console.log("Filtrando")
    const text = document.getElementById("filter_text").value
    const supermarkets = Array.from(document.querySelectorAll(".filter_super")).map(super_product => super_product.id)

    const productsFiltered = products.filter(product =>
        product.name.toUpperCase().includes(text.toUpperCase()) &&
        supermarkets.includes(product.supermarket.id.toString())
    )
    render(productsFiltered)
}