from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    user = request.user.is_authenticated    # 사용자가 인증을 받았는지(로그인이 되어있는지)
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # objects.all : 모든 데이터 불러온다. / .order_by : 데이터 오름차순 정렬로 가져오는데, (-)이므로 반대
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet':all_tweet})
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag','').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error':'내용을 넣어주세요', 'tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content','')

            for tag in tags:
                tag = tag.strip()   # 공백없애준다
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()

        return redirect('/tweet')

@login_required
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def detail_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    # 댓글 모델 가져오기
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment':tweet_comment})

@login_required
def write_comment(request,id):
    if request.method == 'POST':
        comment = request.POST.get('comment','')
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))

@login_required
def delete_comment(request,id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))

# django taggit 사용에 필요한 코드
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context