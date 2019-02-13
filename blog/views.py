from django.shortcuts import render,get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# # Create your views here.

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list,3)#3 post in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         #if page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         #if page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,'blog/post/list.html',{'page':page,'posts':posts})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year =year,
                                publish__month = month,
                                publish__day = day)
    #list of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None

    if request.method == 'POST':
        #a comment is created 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post = post
            #save the comment to the databse
            new_comment.save()
    else:
        comment_form = CommentForm()
    context_dict = {'post':post, 'comments':comments, 'new_comment':new_comment,'comment_form':comment_form}
    return render(request, 'blog/post/detail.html',context_dict)              


#using class based views (detail and list generic view)
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name =  'blog/post/list.html'

from .forms import EmailPostForm

def post_share(request, post_id):
    #retrieve post by id
    post = get_object_or_404(Post, id= post_id, status= 'published')

    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #firm fields passed validation
            cd = form.cleaned_data
            #.. send email
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html',{'post':post,'form':form})