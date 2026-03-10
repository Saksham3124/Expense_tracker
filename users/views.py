from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})