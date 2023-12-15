from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages

User = get_user_model()

def signup(request):
    if request.method =='POST':
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        email = request.POST.get("email")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Un utilisateur avec ce nom d'utilisateur existe déjà.")
            return render(request, 'accounts/signup.html')
        
        user = User.objects.create_user(username=username, 
                                        first_name=firstname, 
                                        last_name=lastname, 
                                        password=password,
                                        email=email)
        
        auth_login(request, user)
        messages.success(request, "Inscription réussie.")
        return redirect('index')
    
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method =='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorect.")
    
    return render(request, 'accounts/login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')
