from django.db import models
from cash.utilities.keys import Keys


class BaseModel(models.Model):
    id = models.CharField(
        max_length=128,
        default=Keys.primarykey,
        editable=False,
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


# user
# admin - marchand - client
# seul les marchands ont un code et un qrcode marchand
# le code permet de retrouver un marchand
# le qrcode pour effectuer un payment
# apres on ajoutera la locatisation en temps reel
class User(BaseModel):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128)
    # role : client - marchand - admin
    role = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    # picture = models.ImageField(upload_to="user")
    fingerprint = models.ImageField(upload_to="fringer")
    # code marchand
    code = models.CharField(max_length=32, null=True, blank=True)
    # qrcode marchand
    qrcode = models.ImageField(upload_to="invoice")


# liste de produit vendu
class Product(BaseModel):
    marchand = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="marchand_product"
    )
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="product")
    price = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)
    unit = models.IntegerField(default=1)


# un panier consu par le client
class Shop(BaseModel):
    client = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="client_shop"
    )
    shop_price = models.DecimalField(
        max_digits=321, decimal_places=2, default=0.0
    )
    # 5% de la commande
    fees = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)


# achat d'un produit avec la quantité souhaité a ajouter au panier
class Shopping(BaseModel):
    client = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="client_shop"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prd_shop"
    )
    qte = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shopp"
    )


# effectuer un payment a partir d'un panier
class Invoice(BaseModel):
    marchand = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="marchand"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client"
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shoppay"
    )


# effectuer un payment letal par facture
class LetalInvoice(BaseModel):
    marchand = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="marchand"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client"
    )
    invoice = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)


# notification suivant les actions
class Notification(BaseModel):
    subject = models.CharField(max_length=128)
    destinate = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sms'
    )
    message = models.TextField()
    read = models.BooleanField(default=False)
