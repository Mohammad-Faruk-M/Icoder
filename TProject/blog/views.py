from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # Add this import

# Create your views here.
def blogHome(request):
    allPost=Post.objects.all()
    context={'allPost':allPost}
    return render(request,'blog/blogHome.html',context)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post)
    context={'post':post, 'comments': comments, 'user': request.user}
    return render(request, "blog/blogPost.html", context)

# Add @login_required decorator
@login_required(login_url='/login')  # This will redirect to login page if not authenticated
def postComment(request):
    if request.method == "POST":
        comment_text=request.POST.get('comment')  # Renamed to avoid conflict
        user=request.user  # Now guaranteed to be authenticated
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        blog_comment=BlogComment(comment=comment_text, user=user, post=post)  # Renamed variable
        blog_comment.save()
        messages.success(request, "Your comment has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")