from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.core.cache import cache

def index(request):
   post_list = Post.objects.all().order_by('-created_at') # 모든 리스트를 작성일시 역순으로
   post_list = post_list[:10]
   board_num = list(range(1, (len(post_list) // 10)+2))

   return render(request, 'freeboard/index.html', {'post_list':post_list, 'board_num':board_num,})

def post_detail(request, pk):
    post = cache.get(str(pk))
    print(post, " : ", type(post))
    print("Mem Cache!")
    if not isinstance(post, Post):
        post = Post.objects.get(pk=pk)
        print("Disk I.O!")
    run_cache_queue(pk, post)
    post.increase_Views()
    return render(request,'freeboard/post_detail.html', {'post':post, })

def write_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) # 중복 DB save를 방지해준다.
            post.ip = request.META['REMOTE_ADDR'] # ip 필드는 유저로 부터가 아닌 프로그램으로 채워넣음.
            post.save()
            return redirect('/freeboard/')
    else:
        form = PostForm()
    return render(request, 'freeboard/write_post.html', {'form':form, })

def show_board(request, pk):
    post_list = Post.objects.all().order_by('-created_at') # 모든 리스트를 작성일시 역순으로
    board_num = list(range(1, (len(post_list) // 10) + 2))
    post_list = post_list[(int(pk)-1)*10 : int(pk)*10]
    return render(request, 'freeboard/index.html', {'post_list': post_list, 'board_num': board_num,})

def run_cache_queue(pk, post):
    cacheList = cache.get('cacheList')
    if cacheList is None:
        cacheList = []
        cache.set(str(pk), post)
        cacheList.append(pk)
        cache.get_or_set('cacheList', cacheList)
    else:
        if pk in cacheList:
            cacheList.remove(pk)
            cacheList.append(pk)
        else:
            cacheList.append(pk)
            cache.set(str(pk), post)
            if len(cacheList) > 10:
                cache.delete(cacheList[0])
                cacheList = cacheList[1:]
        cache.set('cacheList', cacheList)
    print(cacheList)
