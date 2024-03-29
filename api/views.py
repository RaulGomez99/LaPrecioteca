from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Supermarket, Product, User, Favourites, History, Stars
import json
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

import random
import numpy as np

# Create your views here.

def product2json(product, user_id):
    fav = len(Favourites.objects.filter(user__id = user_id , product__id = product.id)) == 1
    rating = Stars.objects.filter(user__id = user_id, product__id = product.id)
    return json.dumps({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "photo": product.product_photo,
        "type": product.type,
        "is_favourite": fav,
        "rating": rating[0].rating if len(rating) > 0 else 0
    })
    
def product2dict(product):
    return dict({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "photo": product.product_photo,
        "type": product.type
    })
    
def historic2json(historic):
    print(historic)
    fecha = historic['data'].strftime("%Y-%m-%d")
    return json.dumps({
        "price": historic['price'],
        "date": fecha
    })
    
def addSuper2Product(product):
    super_product = Supermarket.objects.get(id = product["supermarket"])
    product["supermarket"] = model_to_dict(super_product)
    return product
    
    
def index(request):
    if not request.user.is_authenticated: return redirect("login") 
    products = Product.objects.all()
    
    mercadona = Product.objects.filter(supermarket__name = "Mercadona")
    consum = Product.objects.filter(supermarket__name = "Consum")
    dia = Product.objects.filter(supermarket__name = "Dia")
    carrefour = Product.objects.filter(supermarket__name = "Carrefour")
    
    mercadona_logo = Supermarket.objects.filter(name = "Mercadona")[0].url_logo
    consum_logo = Supermarket.objects.filter(name = "Consum")[0].url_logo
    dia_logo = Supermarket.objects.filter(name = "Dia")[0].url_logo
    carrefour_logo = Supermarket.objects.filter(name = "Carrefour")[0].url_logo

    return render(request, "index.html", context = {
        "hot_products": products,
        "mercadona": mercadona,
        "consum": consum,
        "dia": dia,
        "carrefour": carrefour,
        
        "mercadona_logo": mercadona_logo,
        "consum_logo": consum_logo,
        "dia_logo": dia_logo,
        "carrefour_logo": carrefour_logo
    })
    

def product_by_id(request, id):
    product = Product.objects.filter(id=id)[0]
    data = product2json(product, request.user.id)
    return HttpResponse(data, content_type='application/json')


def product_by_id_view(request, id):
    # Cambiarlo para que devuelva el producto bonito con una view
    product = Product.objects.filter(id=id)[0]

    fav = len(Favourites.objects.filter(user__id = request.user.id , product__id = product.id)) == 1
    
    historic = History.objects.filter(product__id = id)
    historic = [model_to_dict(h) for h in historic]
    historic = list(map(lambda h: dict({"data": h["data"].strftime("%Y-%m-%d"), "price": h["price"]}), historic))
    rating = Stars.objects.filter(user__id = request.user.id, product__id = id)
    if(len(rating)>0):
        rating = rating[0].rating
    else:
        rating = 0

    return render(request, "producto.html", context = {"product" : product2dict(product), "fav": fav, "historical": historic, "rating": rating})
    
def error_404(request, exception):
    return render(request, '404.html', {})


def register(request):
    if request.user.is_authenticated: return redirect("index")
    return render(request, "register.html")

def login_view(request):
    if request.user.is_authenticated: return redirect("index")
    return render(request, "login.html")

def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        error = ""
        users = User.objects.filter(username = data["username"])
        if len(users) > 0: error += "El Usuario ya existe\n"
        users = User.objects.filter(email = data["email"])
        if len(users) > 0: error += "El Email ya existe"
        
        if error == "":
            user = User.objects.create_user(
                first_name = data["name"], 
                last_name = data["surname"],
                email = data["email"],
                phone = data["tlf"],
                username = data["username"],
                password = data["password1"]
            )
            
            user = authenticate(request, username = data["username"], password = data["password1"])
            login(request, user)

            return HttpResponse(json.dumps({"ok":True}), content_type='application/json')
    
    
        return HttpResponse(json.dumps({"error":error}), content_type='application/json')
    else:
        return redirect('register')


def login_user(request):
    data = json.loads(request.body)
    if(data['username']== None): return redirect('login')
    username = data['username']
    password = data['password1']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(json.dumps({"ok":True}), content_type='application/json')
    else:
        error = 'Te has equivocado en el Usuario o la Contraseña'
        return HttpResponse(json.dumps({"error":error}), content_type='application/json')

def logout_view(request):
    logout(request)
    return redirect('login')

def filtro(request):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    products = Product.objects.all()
    clean_products = [model_to_dict(product) for product in products]
    clean_products2 = list(map(addSuper2Product, clean_products))
    supermarkets = Supermarket.objects.all()
    supermarkets_clean = [model_to_dict(supermarket) for supermarket in supermarkets]
    print(supermarkets_clean)
    return render(request, "filtro.html", context = {"products" : clean_products2, "supermarkets": supermarkets_clean})
    
    

def toggle_fav(request, id):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    fav = Favourites.objects.filter(user__id = request.user.id, product__id = id)
    if len(fav) == 1:
        fav.delete()
        return HttpResponse(json.dumps({"ok":"Eliminado de favoritos"}), content_type='application/json')
    else:
        product = Product.objects.get(id = id)
        fav = Favourites(user = request.user, product = product)
        fav.save()
        return HttpResponse(json.dumps({"ok":"Añadido a favoritos"}), content_type='application/json')
    
    
def carrito(request):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    favs = Favourites.objects.filter(user__id = request.user.id)
    products = list(map(lambda fav: fav.product, favs))
    print(products)
    clean_products2 = [model_to_dict(product) for product in products]
    
    mercadona_logo = Supermarket.objects.filter(name = "Mercadona")[0].url_logo
    consum_logo = Supermarket.objects.filter(name = "Consum")[0].url_logo
    dia_logo = Supermarket.objects.filter(name = "Dia")[0].url_logo
    carrefour_logo = Supermarket.objects.filter(name = "Carrefour")[0].url_logo
    
    return render(request, "carrito.html", context = {
        "products" : clean_products2,
        "mercadona_logo": mercadona_logo,
        "consum_logo": consum_logo,
        "dia_logo": dia_logo,
        "carrefour_logo": carrefour_logo
        })

def crearProducto(request):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    if request.method == 'POST':
        data = json.loads(request.body)
        error = ""
        products = Product.objects.filter(name = data["name"])
        if len(products) > 0: error += "El Producto ya existe\n"
        
        if error == "":
            product = Product.objects.create(
                name = data["name"], 
                price = data["price"],
                url_image = data["url_image"],
                url_product = data["url_product"],
                supermarket = Supermarket.objects.get(id = data["supermarket"])
            )
            
            return HttpResponse(json.dumps({"ok":True}), content_type='application/json')
    
    
        return HttpResponse(json.dumps({"error":error}), content_type='application/json')
    else:
        return redirect('filtro')

def obtenerHistoricoProducto(request, id):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    hist = History.objects.filter(product__id = id)
    historical = [model_to_dict(h) for h in hist]
    hist_json = [historic2json(h) for h in historical]
    return HttpResponse(json.dumps({"historical":hist_json}), content_type='application/json')


def scoreRating(request):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    user_id = request.user.id
    print(request.user)
    if request.method == 'POST':
        print("entra")
        data = json.loads(request.body)
        punctuation = Stars.objects.filter(user__id = user_id, product__id = data["product_id"])
        print(punctuation)
        if len(punctuation)>0:
            punctuation[0].rating = data["rating"]
            punctuation = punctuation[0]
        else:
            punctuation = Stars(user = request.user, product = Product.objects.get(id = data["product_id"]), rating = data["rating"])
        punctuation.save()
        return HttpResponse(json.dumps({"ok":True}), content_type='application/json')
    return HttpResponse(json.dumps({"error":"No está entrando con Post"}), content_type='application/json')

def create_random_historic(request):
    products = Product.objects.all()
    
    for product in products:
        for i in range(1, 10):
            if len(History.objects.filter(product__id = product.id, data = "2021-05-0" + str(i))) > 0: continue
            history = History(product = product, price = product.price + random.uniform(-1, 1), data = "2021-05-0" + str(i))
            history.save()
    return HttpResponse(json.dumps({"ok":True}), content_type='application/json')

def mi_perfil(request):
    if not request.user.is_authenticated: return redirect("login")
    return render(request, "mi_perfil.html", context = {"user": request.user})

def edit_user(request):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    if request.method == 'POST':
        data = json.loads(request.body)
        error = ""
        users = User.objects.filter(email = data["email"])
        if len(users) > 0 and users[0].id != request.user.id: error += "El Email ya existe"
        
        if error == "":
            user = User.objects.get(id = request.user.id)
            user.email = data["email"]
            user.first_name = data["name"]
            user.last_name = data["surname"]
            user.phone = data["tlf"]
            
            if(data["password"] != ""): user.set_password(data["password"])
            user.save()
            
            return HttpResponse(json.dumps({"ok":True}), content_type='application/json')
    
    
        return HttpResponse(json.dumps({"error":error}), content_type='application/json')
    return HttpResponse(json.dumps({"error":"No está entrando con Post"}), content_type='application/json')