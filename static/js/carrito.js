window.onload = () => {
    const products = Array.from(document.querySelectorAll(".my-data")).map(product => (
        JSON.parse(product.getAttribute("data-my-data").replace(/'/g, '"'))
    ))
    console.log(products)
}