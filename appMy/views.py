from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

def indexPage(request):
    posts = Post.objects.all().order_by("?")[:4]
    context = {
        "categorys" : Category.objects.all(),
        "posts" : posts,
    }
    return render(request, "index.html", context)

def card_listPage(request, cate="all", grid=4):
    
    if cate  != "all":
        posts = Post.objects.filter(category__title=cate)
    else:
        posts = Post.objects.all()
    categorys = Category.objects.all()    
    context = {
        "posts": posts,
        "cate": cate,
        "grid": grid,
        "categorys": categorys,
    }
    return render(request, "card_list.html", context)

def detailPage(request, pid): # fonksiyonlar ve sayfalar GET ile çalışırlar
    
    comments = Comment.objects.filter(post=pid)
    post = Post.objects.get(id=pid)
    
    if request.method == "POST":
       fullname = request.POST.get("fullname")
       text = request.POST.get("comment")
       
       comment = Comment(full_name = fullname, text = text, post = post)
       comment.save()
    
    
    context={
        "comments" : comments,
        "post": post,
        "categorys" : Category.objects.all(),
    }
    return render(request, "detail.html", context)

# === USER ===

def loginPage(request):
    hata = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password) # kontrol eder, varsa kullanıcı adını yoksa None döndürür
        
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            hata = "Kullanıcı adı veya şifre yanlış"
        
    context = {
        "hata":hata,
    }
    return render(request, "user/login.html", context)


def registerPage(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        check = request.POST.get("check")
        print(check)
        
        if check is not None:
            if password1 == password2:
                # exists filterın içinde değer varsa Tru yoksa False döndürür
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=password2)
                        user.save()
                        return redirect("loginPage")
                    else:
                        hata = "Bu email zaten başkası tarafından kullanılıyor!"
        else:
            hata = "Formu onaylayın"
             
    context = {
       #"hata":hata,
    }
    return render(request, "user/register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("loginPage")
    