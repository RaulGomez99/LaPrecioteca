from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


# Create your models here.
class Supermarket(models.Model):
    name = models.CharField(max_length = 30)
    url_logo = models.TextField(blank = True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length = 300)
    supermarket = models.ForeignKey(Supermarket, on_delete = models.CASCADE, related_name = "products")
    price = models.FloatField(default = 0)
    description = models.TextField(blank = True)
    product_photo = models.TextField(blank = True)
    type = models.CharField(max_length = 100, blank = True)
    
    def __str__(self):
        return self.name
    

# Usuario cambiado
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, first_name=None, last_name=None, phone=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, first_name=None, last_name=None, phone=None):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    
class Stars(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    rating = models.IntegerField()
   
    def __str__(self):
        return self.user.username + str(self.rating)
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "comments")
    comment = models.TextField()
    data = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        print(self.comment)
        user = User.objects.filter(username = self.user)[0]
        self.user = user.id
    
class History(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "history")
    data = models.DateTimeField()
    price = models.FloatField()
    
class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "favs")
    
 