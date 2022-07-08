from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, HttpResponse
from .models import Post, profile, comment, contact_us
import datetime
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    

    return render(request, "index.html")

def land(request):
    return render(request, "index.html")


def about(request):

    return render(request, "about_us.html")

def blog(request):
    post = Post.objects.all().order_by("-views")[:5]

    pro_con={"post":post}
    return render(request, "blog.html", pro_con)

class blogging(CreateView):
    model = Post
    template_name = "blogging.html"
    fields = ["title", "title_tag", "body", "image", "category"]

    def form_valid(self, form):
        slug=form.cleaned_data["title"]
        form.instance.slug=slug
        form.instance.post_date=datetime.timezone.now()
        form.instance.author=self.request.user
        return super().form_valid(form)


def edit_account(request):
    cu_us_id = request.user.id

    all = User.objects.filter(pk=cu_us_id)


    # # last_name=User.last_name
    user = profile.objects.filter(user_id=cu_us_id)
    post=Post.objects.filter(author=request.user)


    pro_con = {"user": user,
               "all": all,
               "post":post

               }
    return render(request, "edit_account.html", pro_con)

def account(request):
    cu_us_id=request.user.id


    all=User.objects.filter(pk=cu_us_id)

    # # last_name=User.last_name
    user=profile.objects.filter(user_id=cu_us_id)



    post=Post.objects.filter(author=request.user)


    pro_con={ "user": user,
              "all":all,
              "post":post
    }
    return render(request, "account.html", pro_con)


def update_account(request):
    cu_us_id = request.user.id

    name=str(request.POST.get("fullname"))
    email=request.POST.get("email")

    phone=request.POST.get("phone")
    mobile=request.POST.get("mobile")
    address=request.POST.get("address")
    facebook=request.POST.get("facebook")
    instagram=request.POST.get("instagram")
    github=request.POST.get("github")
    twitter=request.POST.get("twitter")
    website=request.POST.get("website")
    bio=request.POST.get("bio")

    profile_ =profile.objects.get(user=cu_us_id)
    profile_.phone=phone
    profile_.mobile = mobile
    try:
        profile_.profile_pic=request.FILES["profile_pic"]
    except:
        pass
    profile_.address =address
    profile_.facebook =facebook
    profile_.instagram =instagram
    profile_.github =github
    profile_.Bio=bio
    profile_.website =website
    profile_.twitter =twitter

    profile_.save()

    name=name.split(" ")
    firstname_=True
    firstname = ""
    lastname =""

    for i in name:

        if len(i)>0 and firstname_==True:
            firstname=i

            firstname_=False
        elif len(i)>0 and firstname_==False:
            lastname=i


    user=User.objects.get(username=request.user)
    user.first_name=firstname
    user.last_name =lastname
    user.email=email
    user.save()

    cu_us_id = request.user.id


    all = User.objects.filter(pk=cu_us_id)

    # # last_name=User.last_name
    user = profile.objects.filter(user_id=cu_us_id)
    post=Post.objects.filter(author=request.user).values_list("title").order_by("-views")[:3]
    try:
        post=post[:3]
    except:
        post=post





    pro_con = {"user": user,
               "all": all,
               "post":post
               }
    return render(request, "account.html", pro_con)


def register(request):

    if request.method == "POST":
        user_name=request.POST.get("user_Name")
        fname=request.POST.get("first_name")
        lname=request.POST.get("last_name")
        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        email=request.POST.get("email")

        try:
            user = User.objects.get(username=str(user_name))
        except:
            user=None

        if user is not None:
            messages.error(request, "we are having a existing user with this name, try another user name")

        if user is None:
        # checks for user creation
            if len(user_name)<=30:
                if "@" in email and ".com" in email:
                    if pass1 == pass2:



                            # creating users!!!

                            my_user = User.objects.create_user(user_name, email, pass1)

                            my_user.first_name = fname
                            my_user.last_name = lname
                            my_user.save()
                            messages.success(request, "you have a account")

                            user=User.objects.get(username=str(user_name))

                            profile_=profile.objects.create(user=user)

                            user = authenticate(username=user, password=pass1)
                            login(request, user)





    return render(request, "blog.html")


def handle_login(request):
    if request.method == "POST":
        username_=request.POST.get("loginuser_Name")
        loginpassword1=request.POST.get("loginpasword")

        user = authenticate(username=username_, password=loginpassword1)

        if user is not None:
            login(request, user)
            messages.success(request, "You are Successfully logged in")
            return redirect("blogging")
        elif user is None:
            messages.warning(request, "Warning, You have entered something wrong")
            return redirect("blog")
        else:
            messages.warning(request, "Warning, You have entered something wrong")
            return redirect("blog")

    
def handle_logout(request):
    
    logout(request)
    messages.success(request, "You are Successfully logged out")
    return redirect("blog")

def blog_result(request, slug):
    post = Post.objects.filter(slug=slug)
    try:
        post_=Post.objects.get(slug=slug)

        views=list(post.values_list("views"))[0][0]+1
        post_.views=views
        post_.save()
        post = Post.objects.filter(slug=slug)
    except:
        pass

    con = {"post": post,

           }
    if len(post)==0:
        pass

    else:

        l=list(post.values_list("id"))[0][0]


        com=comment.objects.filter(blog=l)

        con["comment"]=com


    return render(request, "blog_result.html", con)

def search(request):
    qu = request.GET.get('search', '')

    if len(qu) > 50:
        posts = Post.objects.none()
        messages.warning(request, "fill the search box correctly")
    elif qu=="":
        posts=Post.objects.none()
        messages.warning(request, "fill the search box correctly")
    else:
        posts = Post.objects.filter(title__icontains=qu)
        q=Post.objects.filter(id=1).values_list("views")






    post_list={"posts":posts, "qu":qu}
    return render(request, "search_result.html", post_list)


class Edit_Blog(UpdateView):
    model = Post
    template_name = "edit_blog.html"
    fields = ["title", "title_tag", "image", "body", "category"]

    def form_valid(self, form):
        slug = form.cleaned_data["title"]
        form.instance.slug = slug
        form.instance.post_update = datetime.timezone.now()
        return super().form_valid(form)


def comment_add(request):
    cu_us_id = request.user.id
    coment=request.POST.get("comment")
    blog_id=request.POST.get("slug")

    user=User.objects.get(pk=cu_us_id)
    profile_=profile.objects.get(user=user)
    post=Post.objects.get(id=blog_id)

    coment_add=comment.objects.create(name=user, blog=post, profile=profile_, body=coment, date=datetime.datetime.now())

    post = Post.objects.filter(id=blog_id)

    con = {"post": post,

           }
    if len(post) == 0:
        pass

    else:

        l = list(post.values_list("id"))[0][0]
        slugy=list(post.values_list("slug"))[0][0]


        com = comment.objects.filter(blog=l)

        con["comment"] = com

    return render(request, "blog_result.html", con)

def comment_edit(request):

    comment_id=request.POST.get("commentid")
    coment=request.POST.get("comment_body")
    post=request.POST.get("post")


    com_edit=comment.objects.filter(id=comment_id, body=coment)



    post = Post.objects.filter(id=post)
    content = {"comment_edit": com_edit,
               "edit": True,
               "post":post}

    if len(post) == 0:
        pass

    else:

        l = list(post.values_list("id"))[0][0]


        com = comment.objects.filter(blog=l)

        content["comment"] = com
    return render(request, "blog_result.html", content)

def comment_update(request):
    comment_edit_body=request.POST.get("comment_edit_body")
    comment_id=request.POST.get("comment_id")
    post_id=request.POST.get("slug")

    com=comment.objects.get(id=comment_id)
    com.body=comment_edit_body
    com.updated_date=datetime.datetime.now()
    com.save()

    post = Post.objects.filter(id=post_id)

    con = {"post": post,

           }
    if len(post) == 0:
        pass

    else:

        l = list(post.values_list("id"))[0][0]
        slugy = list(post.values_list("slug"))[0][0]


        com = comment.objects.filter(blog=l)

        con["comment"] = com

    return render(request, "blog_result.html", con)

def comment_delete(request):

    comment_id=request.POST.get("comment_id_r")

    post_id=request.POST.get("post_id_r")

    remove_comment=comment.objects.filter(id=comment_id)

    remove_comment.delete()

    post = Post.objects.filter(id=post_id)


    con = {"post": post,

           }
    if len(post) == 0:
        pass

    else:

        l = list(post.values_list("id"))[0][0]
        slugy = list(post.values_list("slug"))[0][0]


        com = comment.objects.filter(blog=l)

        con["comment"] = com

    return render(request, "blog_result.html", con)

def advance_search(request):
    post = Post.objects.all()
    pro=Post.objects.all()
    categories=(
        "Food blogs",
        "Travel blogs",
        "Health and fitness blogs",
        "Lifestyle blogs",
        "Fashion and beauty blogs",
        "Photography blogs",
        "Personal blogs",
        "DIY craft blog",
        "Parenting blogs",
        "Business blogs",
        "Music blogs",
        "Book and writing blogs",
        "Art and design blogs",
        "Interior design blogs",
        "Personal finance blogs",
        "News blogs",
        "Sports blogs",
        "Movie blogs",
        "Religion blogs",
        "Political blogs",
        "others"
    )
    professions=[
        "accountant", "actor", "actress", "air traffic controller", "architect", "artist", "attorney", "banker",
        "bartender", "barber", "bookkeeper", "builder", "businessman", "businesswoman", "businessperson",
        "butcher", "carpenter", "cashier", "chef", "coach", "dental hygienist", "dentist", "designer", "developer",
        "dietician", "doctor", "economist", "editor", "electrician", "engineer", "farmer",
        "filmmaker", "fisherman", "flight attendant", "jeweler", "judge", "lawyer", "mechanic", "musician",
        "nutritionist", "nurse", "optician", "painter", "pharmacist", "photographer", "physician",
        "physician's assistant", "pilot", "plumber", "police officer", "politician", "professor", "programmer",
        "psychologist", "receptionist", "salesman", "salesperson", "saleswoman", "secretary",
        "singer", "surgeon", "teacher", "therapist", "translator", "translator", "undertaker", "veterinarian",
        "videographer", "waiter", "waitress", "writer",
    ]
    con = {"post": post,
           "profile":pro,
           "category":categories,
           "professions":professions}
    return render(request, "advance_search.html", con)

def my_blogs(request):
    cu_us=request.user
    posts=Post.objects.filter(author=cu_us)
    content={"posts":posts}
    return render(request, "myblogs.html", content)

def ecommerce(request):

    return render(request, "test.html")


def chatterbox(request):
    post=Post.objects.all()
    con={"post":post}
    return render(request, "test.html", con)


def contactus(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    phone=request.POST.get("phone")
    subject=request.POST.get("subject")
    desc=request.POST.get("message")

    if name is not None:
        if email is not None:
            if subject is not None:
                if desc is not None:
                    contct=contact_us.objects.create(name=name, email=email, phone=phone, subject=subject, description=desc)
                    messages.success(request, str(name), "Your message has been delivered, wait for our reply")

    return render(request, "blog.html")

def like_page(request):
    like=str(request.POST.get("like"))

    like = like.split(" ")
    user=like[1]
    post_id=like[0]




    post=Post.objects.get(id=post_id)
    P=Post.objects.filter(id=post_id)

    url=P.values_list("slug")[0][0]
    post.likes.add(request.user.id)

    post = Post.objects.filter(id=post_id)


    con = {"post": post,

           }
    if len(post) == 0:
        pass

    else:

        l = list(post.values_list("id"))[0][0]
        slugy = list(post.values_list("slug"))[0][0]


        com = comment.objects.filter(blog=l)

        con["comment"] = com

    return render(request, "blog_result.html", con)

def advance_search_work(request):
    title=request.POST.get("title")
    author=request.POST.get("author")
    Category2=request.POST.get("Category2")
    date=request.POST.get("date")
    likes_blog=request.POST.get("likes_blog")
    views_blog=request.POST.get("views_blog")
    Category1=request.POST.get("Category1")
    search_input=request.POST.get("search_input")


    if search_input != "" and search_input is not None:
        search_input_list=Post.objects.filter(Q(title__icontains=search_input) | Q(title_tag__icontains=search_input)).distinct()
    else:
        search_input_list=[]

    if Category1 != "categories" and Category1 is not None:
        Cat1=Post.objects.filter(category__icontains=Category1)
    else:
        Cat1=[]

    if title != "" and title is not None:
        post_title=Post.objects.filter(title__icontains=title)
    else:
        post_title=[]



    if author != "" and title is not None:
        author_list=[]
        user=User.objects.filter(username__icontains=author).values_list("id")

        for index in user:
            for i in index:


                for y in Post.objects.filter(id=i):
                    author_list.append(y)

    else:
        author_list=[]



    if Category2 != "categories" and Category2 is not None:
        Cat2=Post.objects.filter(category__icontains=Category2)
    else:
        Cat2=[]
    if date != "" and date is not None:
        date_list=Post.objects.filter(post_date__icontains=date)
    else:
        date_list=[]
    if likes_blog=="on" and likes_blog is not None:
        likes_list=Post.objects.all().order_by("-likes")
    else:
        likes_list=[]
    if views_blog=="on" and views_blog is not None:
        views_list=Post.objects.all().order_by("-views")
    else:
        views_list=[]

    result_list=list(chain(author_list, search_input_list, post_title, Cat2,Cat1, date_list, likes_list, views_list))


    final_list=[]
    for item in result_list:
        if item not in final_list:
            final_list.append(item)




    p=Paginator(final_list, 1)
    posts=p.get_page(1)


    content={
        "posts":posts,
        "permission_post": True

    }

    return render(request, "advance_search_result.html", content)

def advance_search_users(request):
    profession=request.POST.get("profession")
    author=request.POST.get("author")
    Male=request.POST.get("Male")
    Female=request.POST.get("Female")
    Trans=request.POST.get("Transgender")


    li=[profession, author, Male,Female, Trans]
    li_approved=[]
    for item in li:
        if item!=None:
            li_approved.append(item)





    if profession!="profession" and profession is not None:
        user_profession=profile.objects.filter(Profession__icontains=profession)
    else:
        user_profession=[]

    if author != "" and author is not None:
        author_list = []
        user = User.objects.filter(username__icontains=author).values_list("id")

        for index in user:
            for i in index:

                for y in profile.objects.filter(id=i):
                    author_list.append(y)

    else:
        author_list = []

    if Male=="on" and Male is not None:
        user_male=profile.objects.filter(Gender__icontains="M")

    else:
        user_male=[]
    if Female=="on" and Female is not None:
        user_female=profile.objects.filter(Gender__icontains="F")

    else:
        user_female=[]
    if Trans=="on" and Trans is not None:
        user_trans=profile.objects.filter(Gender__icontains="T")

    else:
        user_trans=[]

    result_list=list(chain(author_list,user_profession, user_male, user_trans, user_female))

    final=[]
    for item in result_list:
        if item not in final:
            final.append(item)




    con={
        "users":final,
        "permission_post":False,
        "posts":'####'
    }

    return render(request, "advance_search_result.html", con)
