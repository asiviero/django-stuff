from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from social_list.models import Player, PlayerForm, UserForm

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
            form = UserForm(request.POST)
            form_player = PlayerForm(request.POST)
            if form.is_valid() and form_player.is_valid():
                new_user = form.save()
                username = request.POST.get('username')
                password = request.POST.get('password1')

                # Player
                new_player = form_player.save(commit = False)
                new_player.user = new_user
                new_player.save()

                user = authenticate(username=username,password=password)
                login(request,user)
                return redirect(request.POST.get('next'))

    else:
        pass
    return render(request,'login_register.html', {
        "login_form" : AuthenticationForm,
        "user_creation_form" : UserForm,
        "player_form" : PlayerForm,
        "next" : request.GET.get("next")
    })
