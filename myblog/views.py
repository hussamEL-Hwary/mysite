from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.

def single_slug(request, slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if slug in categories:
        # Get all sreises
        matching_serieses = TutorialSeries.objects.filter(tutorial_category__category_slug=slug)

        series_urls = {}
        for m in matching_serieses.all():
            part = Tutorial.objects.filter(series__tutorial_series=m.tutorial_series).first()
            print(part)
            series_urls[m] = part
        return render(request=request, 
                      template_name='main/category_series.html',
                      context={"tutorial_series": matching_serieses,  "part_ones": series_urls})
    
    tutorials = [tut.slug for tut in Tutorial.objects.all()]
    print(tutorials)
    print(slug)
    if slug in tutorials:
        this_tut = Tutorial.objects.get(slug=slug)
        tutorials_from_series = Tutorial.objects.filter(series__tutorial_series=this_tut.series)
        this_tutorial_idx = list(tutorials_from_series).index(this_tut)
        return render(request=request, 
                      template_name='main/tutorials.html',
                      context={"tutorial": this_tut, 
                                "sidebar": tutorials_from_series,
                                "this_tut_idx": this_tutorial_idx})
    
    return HttpResponse("Surprice Nothing found")


def homepage(request):
    return render(request=request, 
                  template_name='main/category.html', 
                  context={'categories': TutorialCategory.objects.all})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, f"New Account created: {user_name}")
            login(request, user)
            return redirect("blog:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
    form = NewUserForm
    return render(request=request, 
                  template_name='main/register.html', 
                  context={"form": form})


def logout_user(request):
    logout(request)
    messages.info(request, "loged out successfully!")
    return redirect("blog:homepage")


def login_user(request):
    # get: return login form
    # post: validate and authenticate
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = authenticate(username=username, password=password)

            if user is not None:
                print(user.password)
                login(request, user)
                messages.info(request, f"successfully logged in!")
                return redirect("blog:homepage")
            else:
                 messages.error(request, "Invalid username or password.")
        else:
             messages.error(request, "Invalid username or password.")
    form = AuthenticationForm
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})
