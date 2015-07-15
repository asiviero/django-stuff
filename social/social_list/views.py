from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")

def login_and_register(request):

    if request.method == 'POST':
        if request.POST.get("form") == "login_form":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect(request.POST.get('next'))
        elif request.POST.get("form") == "user_creation_form":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                username = request.POST.get('username')
                password = request.POST.get('password1')
                user = authenticate(username=username,password=password)
                login(request,user)
                return redirect(request.POST.get('next'))

    else:
        print("ao")
    return render(request,'login_register.html', {
        "login_form" : AuthenticationForm,
        "user_creation_form" : UserCreationForm,
        "next" : request.GET.get("next")
    })
