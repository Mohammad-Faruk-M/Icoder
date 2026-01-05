from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    # return HttpResponse("This is home page")
    return render(request,'home/home.html')
def about(request):
    # return HttpResponse("This is about page")
    return render(request,'home/about.html')
def contact(request):
    # return HttpResponse("This is contact page")
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<4 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly.")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your messages has been successfully sent.")
    return render(request, 'home/contact.html')

def search(request):
    query=request.GET.get('query','')
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handlesignup(request):
    #Get the post parameters
    if request.method =="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['pass1']
        repassword=request.POST['pass2']
        #Check for errornous inputs
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
            return redirect("/")
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect("/")
        if password!=repassword:
            messages.error(request,"Passwords do not match")
            return redirect("/")
        #Create the user
        user=User.objects.create_user(username,email,password)
        user.first_name=fname
        user.last_name=lname
        user.save()
        messages.success(request,"Your account has been created successfully")
        return redirect("/")

    else:
        return HttpResponse("404 - Not Found")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
def handelLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect("/")
    