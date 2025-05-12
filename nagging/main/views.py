from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def report(request):
    return render(request, 'main/report.html')

def helper(request):
    return render(request, 'main/helper.html')

def settings(request):
    return render(request, 'main/settings.html')
