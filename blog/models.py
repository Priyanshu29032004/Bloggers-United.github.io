from ckeditor.fields import RichTextField
from django.db import models

from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    Gender_Choices=(
        ("Male", "M"),
        ("Female", "F"),
        ("Transgender", "T")
    )

    professions= (
        ("accountant", "accountant"),
        ("actor", "actor"),
        ("actress", "actress"),
        ("air traffic controller", "air traffic controller"),
        ("architect", "architect"),
        ("artist", "artist"),
        ("attorney", "attorney"),
        ("banker", "banker"),
        ("bartender", "bartender"),
        ("barber", "barber"),
        ("Blogger", "Blogger"),
     ( "bookkeeper", "bookkeeper"),
     ("builder", "builder"),
     ("businesswoman", "businesswoman"),
     ("businessperson", "businessperson"),
     ("butcher", "butcher"),
     ("carpenter", "carpenter"),
     ("cashier", "cashier"),
     ("chef", "chef"),
     ("coach", "coach"),
     ("dental hygienist", "dental hygienist"),
     ("dentist", "dentist"),
     ("designer", "designer"),
     ("developer", "developer"),
     ("dietician", "dietician"),
      ("doctor", "doctor"),
      ("economist", "economist"),
      ("editor", "editor"),
      ("electrician", "electrician"),
      ("engineer", "engineer"),
      ("farmer", "farmer"),
      ("filmmaker", "filmmaker"),
      ("fisherman", "fisherman"),
      ("flight attendant", "flight attendant"),
      ("jeweler", "jeweler"),
      ("judge", "judge"),
      ("lawyer", "lawyer"),
      ("mechanic", "mechanic"),
      ("musician", "musician"),
      ("nutritionist", "nutritionist"),
      ("nurse", "nurse"),
      ("optician", "optician"),
      ("painter", "painter"),
      ("pharmacist", "pharmacist"),
      ("photographer", "photographer"),
      ("physician", "physician"),
      ("physician's assistant", "physician's assistant"),
      ("pilot", "pilot"),
      ("plumber", "plumber"),
      ("police officer","police officer"),
      ("politician", "politician"),
      ("professor", "professor"),
      ("programmer", "programmer"),
      ("psychologist", "psychologist"),
      ("receptionist", "receptionist"),
      ("salesman", "salesman"),
      ("salesperson", "salesperson"),
      ("saleswoman", "saleswoman"),
      ("secretary", "secretary"),
      ("singer", "singer"),
      ("surgeon", "surgeon"),
      ("teacher", "teacher"),
      ("therapist", "therapist"),
      ("translator", "translator"),
      ("undertaker", "undertaker"),
      ("veterinarian", "veterinarian"),
      ("videographer", "videographer"),
      ("waiter", "waiter"),
      ("waitress", "waitress"),
      ("writer", "writer"),
      ("others", "others")
    )

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, upload_to="image", default="avatar.png")
    Gender=models.CharField(max_length=15, choices=Gender_Choices, null=True)
    Profession=models.CharField(max_length=50, choices=professions ,default="Blogger")
    phone=models.PositiveIntegerField(default=0000000000, null=True)
    mobile=models.PositiveIntegerField(default=0000000000, null=True)
    address=models.CharField(max_length=50, null=True)
    Bio=models.TextField(max_length=2000, null=True)
    github=models.URLField(max_length=150, default='',null=True )
    facebook=models.URLField(max_length=150, default='',null=True)
    website=models.URLField(max_length=150, default='',null=True)
    twitter=models.URLField(max_length=150, default='',null=True)
    instagram=models.URLField(max_length=150, default='',null=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    categories_choices=(
        ("Food blogs", "Food blogs"),
        ("Travel blogs", "Travel blogs"),
        ("Health and fitness blogs", "Health and fitness blogs"),
        ("Lifestyle blogs", "Lifestyle blogs"),
        ("Fashion and beauty blogs", "Fashion and beauty blogs"),
        ("Photography blogs", "Photography blogs"),
        ("Personal blogs", "Personal blogs"),
        ("DIY craft blogs", "DIY craft blogs"),
        ("Parenting blogs", "Parenting blogs"),
        ("Music blogs", "Music blogs"),
        ("Business blogs", "Business blogs"),
        ("Art and design blogs", "Art and design blogs"),
        ("Book and writing blogs", "Book and writing blogs"),
        ("Personal finance blogs", "Personal finance blogs"),
        ("Interior design blogs", "Interior design blogs"),
        ("Sports blogs", "Sports blogs"),
        ("News blogs", "News blogs"),
        ("Movie blogs", "Movie blogs"),
        ("Religion blogs", "Religion blogs"),
        ("Political blogs", "Political blogs"),
        ("others", "others")
    )


    title=models.CharField(max_length=50)
    title_tag=models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="media_blog", default="image_blog.png", null=True)
    body=RichTextField(blank=True, null=True)
    post_date=models.DateTimeField()
    post_update=models.DateTimeField(null=True)
    category=models.CharField(max_length=50, choices=categories_choices, null=True)
    likes=models.ManyToManyField(User, related_name="user")
    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("blog")


class comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date =models.DateTimeField()
    updated_date =models.DateTimeField(null=True)

    def __str__(self):
        return str(self.blog) + " by " + str(self.name)

class contact_us(models.Model):
    name=models.CharField(max_length=15)
    email=models.EmailField()
    phone=models.PositiveIntegerField(null=True)
    subject=models.TextField(max_length=60)
    description=models.TextField(max_length=500)

    def __str__(self):
        return str(self.name) + " - " + str(self.subject)


