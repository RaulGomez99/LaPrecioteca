"""LaPrecioteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path("product/<int:id>/", views.product_by_id, name = "product"),
    path("product_info/<int:id>/", views.product_by_id_view, name = "product_view"),
    path("register/", views.register, name = "register"),
    path("register_user", views.register_user, name = "register_user"),
    path("login/", views.login_view, name = "login"),
    path("login_user", views.login_user, name = "login_user"),
    path("logout/", views.logout_view, name = "logout"),
    path("mi_perfil/", views.mi_perfil, name = "mi_perfil"),
    path("filtro/", views.filtro, name = "filtro"),
    path("toggle_fav/<int:id>", views.toggle_fav, name = "toggle_fav"),
    path("favoritos/", views.carrito, name = "carrito"),
    path("historial/<int:id>", views.obtenerHistoricoProducto, name = "historial"),
    path("rate_product/", views.scoreRating, name = "rate_product"),
    path("create_random_historic/", views.create_random_historic, name = "create_random_historic"),
    path("edit_user/", views.edit_user, name = "edit_user")
]