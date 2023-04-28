from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Supermarket, Product, User, Favourites, History
import json
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

# Create your views here.

def product2json(product, user_id):
    fav = len(Favourites.objects.filter(user__id = user_id , product__id = product.id)) == 1
    return json.dumps({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "photo": product.product_photo,
        "type": product.type,
        "is_favourite": fav
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
    data = product2json(product, request.user.id)
    return HttpResponse(data, content_type='application/json')
    
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
    clean_products2 = [model_to_dict(product) for product in products]
    
    return render(request, "carrito.html", context = {"products" : clean_products2})

def crearProducto(request):
    pass

def obtenerHistoricoProducto(request, id):
    if not request.user.is_authenticated: return HttpResponse(json.dumps({"error":"No está logueado"}), content_type='application/json')
    hist = History.objects.filter(product__id = id)
    historical = [model_to_dict(h) for h in hist]
    print(json.dumps({"historical":historical}))
    return HttpResponse(json.dumps({"historical":historical}), content_type='application/json')
    