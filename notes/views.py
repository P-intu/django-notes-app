from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import Signup_form, Noteform
from django.contrib import messages


# Create your views here.

def login_user(request):
    if request.method=="POST":
          username=request.POST.get('username')
          password=request.POST.get('password')
          user=authenticate(username=username,password=password)
          if user is not None:
                login(request,user)
                messages.success(request,'loged in successfuly!')
                return redirect('notes_home')
          else:
                messages.error(request,'invalid username or password')
                
    return render(request, 'notes/login.html')
def signup_user(request):
     if request.method=="POST":
           form=Signup_form(request.POST)
           if form.is_valid():
                 user=form.save(commit=False)
                 user.set_password(form.cleaned_data['password'])
                 user.save()
                 messages.success(request,"account created successfully! plese login.")
                 return redirect('login')
           else:
                request.session['signup_errors']=form.errors
                return redirect('signup')
     else:
      form=Signup_form()
      errors=request.session.pop('signup_errors',None)
      return render(request, 'notes/signup.html',{'form':form, 'errors':errors})
          
    
def logout_user(request):
     logout(request)
     return redirect("firstpage")



def home(request):

     if request.user.is_authenticated:
      search=request.GET.get("search","")
      notes=Note.objects.filter(owner=request.user).order_by('-pinned','-created_at')
      if search:
           notes=notes.filter(title__icontains=search)| notes.filter(content__icontains=search)
     else:
          return redirect('firstpage')
     return render(request, 'notes/home.html',{'notes':notes,'search':search})

@login_required(login_url='login')
def view_note(request,id):
         note = get_object_or_404(Note,id=id,owner=request.user)
         return render(request, 'notes/view_note.html',{'notes':note})

@login_required(login_url='login')
def edit_note(request,id):
     note=get_object_or_404(Note,id=id, owner=request.user)
     if request.method=="POST":
          forms=Noteform(request.POST,instance=note)
          if forms.is_valid():
               forms.save()
               messages.success(request,' Note updated successfully')
               return redirect('view',id=id)
     else:
           forms=Noteform(instance=note)
     return render(request, 'notes/edit_note.html', {'form':forms,'note':note})


@login_required(login_url='login')
def delete_note(request,id):
     note=get_object_or_404(Note,id=id, owner=request.user)
     if request.method=="POST":
             note.delete()
             messages.success(request,' Note deleted successfully')
     return redirect('notes_home')

@login_required(login_url='login')
def add_note(request):
     if request.method=="POST":
          forms=Noteform(request.POST)
          if forms.is_valid():
               note=forms.save(commit=False)
               note.owner=request.user
               forms.save()
               messages.success(request,' Note added successfully')
               return redirect('notes_home')
     else:
          forms=Noteform()
     return render(request, 'notes/add_note.html', {'form':forms})


def firstpage(request):
#      notes=Note.objects.filter(owner=request.user).order_by('-created_at')
     return render(request, 'notes/firstpage.html')


def toggle_pin(request,id):
     note=get_object_or_404(Note,id=id,owner=request.user)
     note.pinned= not note.pinned
     note.save()
     if note.pinned:
          messages.success(request,"note pinned")
     else:
          messages.info(request,"note unpinned successfully")
     return redirect('notes_home')