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
    infoProduct.innerHTML = "<span>Descripción:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>"
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

    const div_rating = document.createElement("div")
    div_rating.classList.add("rating")
    div_rating.id = product.id
    const div_rating_flex = document.createElement("div")
    div_rating_flex.classList.add("rating_flex")

    for (let i = 0; i < 5; i++) {
        const div_rating_star = document.createElement("i")
        div_rating_star.classList.add("rating__star")
        div_rating_star.classList.add("far")
        div_rating_star.classList.add("fa-star")
        div_rating_star.classList.add("fa-xl")
        div_rating_flex.appendChild(div_rating_star)
    }
    div_rating.appendChild(div_rating_flex)

    divPopUp.appendChild(crossMark)
    divPopUp.appendChild(titleProduct)
    imageProductDiv.appendChild(imageProduct)
    divPopUp.appendChild(imageProductDiv)
    infoProduct.appendChild(div_rating)
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

    

    const ratingStars = [...document.getElementsByClassName("rating__star")];
    const ratingValue = product.rating;
    console.log(ratingValue)

    executeRating(ratingStars);
    if(ratingValue>0)  ratingStars[ratingValue - 1].click();
}

function removePopUp() {
    const insert = document.getElementById("insert_popup")
    insert.innerHTML = ""
    const body = document.getElementsByTagName("body")[0]
    body.style.overflow = "auto"
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

function executeRating(stars) {
    const starClassActive = "rating__star fas fa-star fa-xl";
    const starClassInactive = "rating__star far fa-star fa-xl";
    const starsLength = stars.length;
    let i;
    stars.map((star) => {
        star.onclick = async () => {
            const csrftoken = getCookie('csrftoken')
            i = stars.indexOf(star);
            for (i; i >= 0; --i) stars[i].className = starClassActive;
            i = stars.indexOf(star);
            if(i<=3){
                i++
                for(i; i<starsLength; ++i) {
                    stars[i].className = starClassInactive;
                }
            }
            i = stars.indexOf(star)+1;
            const req = await fetch("/rate_product/", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    product_id: stars[0].parentElement.parentElement.id,
                    rating: i
                })
            })
            const json = await req.json()
            if(json.error) alert(json.error)
            console.log(json)
        };
    });
}