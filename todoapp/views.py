from django.shortcuts import render,redirect
from django.views.generic import View
from todoapp.forms import UserForm,SignInForm,TodoForm
from todoapp.models import Todos
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.
def signin_required(fn):
   def wrapper(request,*args,**kwargs):
      if not request.user.is_authenticated:
         return redirect("signin")
      else:
         return fn(request,*args,**kwargs)
   return wrapper


def ownerpermission_required(fn):
   def wrapper(request,*args,**kwargs):
      id=kwargs.get("pk")
      todo_object=Todos.objects.get(id=id)
      if todo_object.user !=request.user:
         logout(request)
         return redirect("signin")
      else:
         return fn(request,*args,**kwargs)
   return wrapper


decs=[signin_required,ownerpermission_required]
       

class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
        
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            print("account")
            return redirect("register")  
        else:
            return render(request,"register.html",{"form":form})
                
class SignInView(View):
    def get(self,request,*args,**kwargs):
      form=SignInForm()
      return render(request,"Login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
      form=SignInForm(request.POST)

      if form.is_valid():
          uname=form.cleaned_data.get("username")
          pwd=form.cleaned_data.get("password")
          user_object=authenticate(request,username=uname,password=pwd)
          if user_object:
            login(request,user_object)
            print("valid ")

            return redirect ("index")
          else:
            print("invalid ")
            return render(request,"Login.html",{"form":form})
      else:
            return render(request,"Login.html",{"form":form})
      
@method_decorator(signin_required,name="dispatch")
class IndexView(View):
   def get(self,request,*args,**kwargs):
      form=TodoForm()
      qs=Todos.objects.filter(user=request.user)
      pending_count=Todos.objects.filter(status="todo",user=request.user).count()
      inprogress_count=Todos.objects.filter(status="inprogress",user=request.user).count()
      finished_count=Todos.objects.filter(status="completed",user=request.user).count()
      print(finished_count)


      return render(request,"index.html",{"form":form,"data":qs,
                                          "finished":finished_count,
                                          "pending":pending_count,
                                          "inprogress":inprogress_count})
   def post(self,request,*args,**kwargs):
      form=TodoForm(request.POST)
      if form.is_valid():
         form.instance.user=request.user
         form.save()
         return redirect("index")
      else:
         return render(request,"index.html",{"form":form})

@method_decorator(decs,name="dispatch")
class TodoUpdateView(View):
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      
      if "status" in request.GET:
         value=request.GET.get("status")
         if value=="inprogress":
            Todos.objects.filter(id=id).update(status="inprogress")
         elif value=="completed":
            Todos.objects.filter(id=id).update(status="completed")
      return redirect("index")     
       
@method_decorator(decs,name="dispatch")
class TodoDeleteView(View):
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      Todos.objects.filter(id=id).delete()
      return redirect("index")


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
   def get(self,request,*args,**kwargs):
      logout(request)
      return redirect("signin")





