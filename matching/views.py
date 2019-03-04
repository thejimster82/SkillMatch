from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


#Creates the login webpage by referencing the html file
def login(request):
    return render(request, 'login.html')


#Creates the home page by referencing the html file
def home(request):
    return render(request, 'home.html')

#Creates the register webpage by referencing the html file
#Uses post method to send the data
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = UserCreationForm()

        args = {'form': form}
        return render(request, 'register.html', args)
