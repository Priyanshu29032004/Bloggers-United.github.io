from django.contrib import admin

from blog.models import comment, Post, profile,contact_us

# Register your models here.
admin.site.register(profile)
admin.site.register(Post)
admin.site.register(comment)
admin.site.register(contact_us)