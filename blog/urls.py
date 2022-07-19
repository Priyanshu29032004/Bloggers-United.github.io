from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import blogging, Edit_Blog

urlpatterns = [
    path("", views.land, name="land"),
    path("search", views.search, name="search"),
    path("index", views.index, name="index"),
    path("about_us", views.about, name="about"),
    path("blog", views.blog, name="blog"),
    path("chatter-box", views.chatterbox, name="chatter-box"),
    path("e-commerce", views.ecommerce, name="e-commerce"),
    path("blogging", blogging.as_view() , name="blogging"),
    path("account", views.account, name="account"),
    path("register", views.register, name="register"),
    path("see_account", views.see_account, name="see_account"),
    path("comment_add", views.comment_add, name="comment_add"),
    path("comment_edit", views.comment_edit, name="comment_edit"),
    path("comment_update", views.comment_update, name="comment_update"),
    path("comment_delete", views.comment_delete, name="comment_delete"),
    path("advance_search", views.advance_search, name="advance_search"),
    path("advance_search_work", views.advance_search_work, name="advance_search_work"),
    path("advance_search_users", views.advance_search_users, name="advance_search_users"),
    path("my_blogs", views.my_blogs, name="my_blogs"),
    path("like_page", views.like_page, name="like_page"),
    path("handle_login", views.handle_login, name="handle_login"),
    path("handle_logout", views.handle_logout, name="handle_logout"),
    path("edit_account", views.edit_account, name="edit_account"),
    path("update_account", views.update_account, name="update_account"),
    path("contact_us", views.contactus, name="contact_us"),
    path("<int:pk>", Edit_Blog.as_view(), name="edit_blog"),
    path('<str:slug>', views.blog_result, name="blog_result"),
    path("<int:pk>", Edit_Blog.as_view(), name="edit_blog"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
