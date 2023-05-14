window.onload = () => {
    const ratingStars = [...document.getElementsByClassName("rating__star")];
    const rating = document.getElementById("rating");
    const ratingValue = rating.getAttribute("data-my-data");
    let hist = getData()
    if (hist.length > 80) hist = hist.slice(hist.length - 80, hist.length)
    document.querySelectorAll(".carrito").forEach(product => {
        product.addEventListener("click", async ev => {
            const id = ev.target.id
            const resp = await fetch("/toggle_fav/" + id)
            const json = await resp.json()
            console.log(json)
            if (json.ok) ev.target.classList.toggle("fav")
            else alert(json.error)
        })
    })

    const grafica = document.querySelector("#grafica");
    const etiquetas = hist.map(h => h.data);
    const hist2020 = {
        label: "Historico precios",
        data: hist.map(h => h.price),
        backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color de fondo
        borderColor: 'rgba(54, 162, 235, 1)', // Color del borde
        borderWidth: 1,// Ancho del borde
    };

    console.log(etiquetas)
    new Chart(grafica, {
        type: 'line',
        data: {
            labels: etiquetas,
            datasets: [
                hist2020,
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 30,
                        maxRotation: 45,
                        minRotation: 45
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontSize: 30
                    }
                }]
            }
        }
    });
    executeRating(ratingStars);
    ratingStars[ratingValue - 1].click();

    
}

function getData() {
    hist = Array.from(document.querySelectorAll(".my-data")).map(product => (
        JSON.parse(product.getAttribute("data-my-data").replace(/'/g, '"'))
    ))
    hist = hist.sort((a, b) => (a.data > b.data) ? 1 : -1)
    return hist
}


function executeRating(stars) {
    const starClassActive = "rating__star fas fa-star fa-2xl";
    const starClassInactive = "rating__star far fa-star fa-2xl";
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
                    product_id: document.querySelectorAll(".carrito")[0].id,
                    rating: i
                })
            })
            const json = await req.json()
            if(json.error) alert(json.error)
            console.log(json)
        };
    });
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