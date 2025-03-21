from django.shortcuts import render,redirect,get_object_or_404
from .models import Task 
from .forms import TaskForm


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    return render(request,'myapp/signup.html',{'form':form})

def signin(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form =AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('task_list')
    return render(request,'myapp/signin.html',{'form':form})
@login_required
def signout(request):
    logout(request)
    return redirect('signin')




@login_required
def create_task(request):
    form=TaskForm()
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.user=request.user
            task.save()          
            return redirect('task_list')
    return render(request,'myapp/task_form.html',{'form':form})
@login_required
def task_list(request):
    # tasks=Task.objects.all()
    tasks= Task.objects.filter(user=request.user)
    return render(request,'myapp/task_list.html',{'tasks':tasks})

@login_required
def task_details(request,slug):
    tasks=get_object_or_404(Task,slug=slug)
    return render(request,'myapp/task_details.html',{'tasks':tasks})

@login_required
def task_update(request,slug):
    task=get_object_or_404(Task,slug=slug,user=request.user)
    form=TaskForm(instance=task)
    if request.method == 'POST':
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    return render(request,'myapp/task_form.html',{'form':form})

@login_required
def task_delete(request,slug):
    task=get_object_or_404(Task,slug=slug,user=request.user)
    task.delete()
    return redirect('task_list')