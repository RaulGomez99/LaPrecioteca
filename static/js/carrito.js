let products;
let mercadona, consum, dia, carrefour;

window.onload = () => {
    products = Array.from(document.querySelectorAll(".my-data")).map(product => (
        JSON.parse(product.getAttribute("data-my-data").replace(/'/g, '"'))
    ))
    mercadona = products.filter(product => product.supermarket == 1)
    consum = products.filter(product => product.supermarket == 3)
    dia = products.filter(product => product.supermarket == 2)
    carrefour = products.filter(product => product.supermarket == 4)
    console.log(products)

    document.getElementById("main_content").innerHTML = ""
    if(mercadona.length) render(mercadona, "mercadona")
    if(consum.length) render(consum, "consum")
    if(dia.length) render(dia, "dia")
    if(carrefour.length) render(carrefour, "carrefour")

}

function render(products, supermarket) {
    const div_super = document.createElement("div")
    div_super.classList.add("supermarket")
    div_super.id = supermarket
    div_title = document.createElement("div")
    div_title.classList.add("title")
    div_title.classList.add(supermarket)
    div_title.innerText = supermarket[0].toUpperCase() + supermarket.slice(1)

    const products_table = document.createElement("div")
    products_table.classList.add("products_table")

    products.forEach(product => {
        const productDiv = document.createElement("a")
        productDiv.href = "/product_info/" + product.id
        productDiv.target = "blank"
        productDiv.classList.add("product_sup")
        productDiv.id = product.id
        const img_product = document.createElement("img")
        img_product.src = product.product_photo
        img_product.classList.add("image")
        img_product.loading = "lazy"
        productDiv.appendChild(img_product)
        const textDiv = document.createElement("div")
        textDiv.classList.add("text")
        textDiv.classList.add(supermarket)
        textDiv.innerHTML = `<span class="centrar"><strong>${product.name}</strong>&nbsp; ${product.price}€</span>`
        productDiv.appendChild(textDiv)
        products_table.appendChild(productDiv)
    })

    div_super.appendChild(div_title)
    div_super.appendChild(products_table)


    const div_insert = document.getElementById("main_content")
    div_insert.appendChild(div_super)
    
}