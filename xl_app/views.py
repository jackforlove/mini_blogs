from django.shortcuts import render,HttpResponse,redirect
from xl_app import models
from django.urls import reverse
from django import forms
from django.db import transaction
from django.forms import widgets,fields
from django.views.decorators.csrf import csrf_exempt,csrf_protect
class ArticleForm(forms.Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control','placeholder': '文章内容'})
    )
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Articl.type_choices)
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # self.fields['artcate'].choices = models.Artcate.objects.filter(blog_id=1).values_list('id','caption')

# Create your views here.
def article(request,**kwargs):
    if request.session.get('is_login',None):
        user=request.session.get('user',None)
        dic={}
        cate_id=models.UserInfo.objects.filter(username=user).first().cate.id
        # for k,v in kwargs.items():
        #     kwargs[k]=int(v)
        #     if v =='0':
        #         pass
        #     else:
        #         dic[k]=v
        req=models.Articl.objects.filter(article_type_id=int(kwargs['artcate_id']),cate=cate_id)

        art_cate=models.Articl.type_choices
        cate=models.Cate.objects.all()
        return render(request,'article.html',{
            'req':req,
            'art_cate':art_cate,
            'cate':cate,
            'kwgrgs':kwargs,
            'cate_id':cate_id
        })
    else:
        return HttpResponse("请先登陆")
def index(request,):
    article_list = models.Articl.objects.all()
    article_type_list = models.Articl.type_choices
    if request.session.get('is_login',None):
      user = request.session['user']
      cate_id=models.UserInfo.objects.filter(username=user).first().cate.id
    else:
        cate_id=None
    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_list': article_type_list,
            'article_type_id': None,
            'cate_id':cate_id
        }
    )

class Fm(forms.Form):
    user=forms.CharField(error_messages={'required':'用户名不能为空','max_length':'用户名过长','min_length':'用户名太短'},max_length=12,min_length=1
                     )
    pwd=forms.CharField(error_messages={'required':'密码不能为空','max_length':'密码过长','min_length':'密码太短'},max_length=12,min_length=2,widget=widgets.PasswordInput)
# 带有session的验证

@csrf_exempt
def login(request):
    if request.method=='GET':
        obj=Fm()
        return render(request,'login.html',{'obj':obj})
    elif request.method=='POST':
        obj=Fm(request.POST)
        ob_1=obj.is_valid()
        if ob_1:
            u=request.POST.get('user')
            p=request.POST.get('pwd')
            user=models.UserInfo.objects.filter(username=u)
            pwd=models.UserInfo.objects.filter(password=p)
            if user and pwd:
                request.session['user']=u
                request.session['is_login']=True
                cate_id=models.UserInfo.objects.filter(username=u).first().cate.id
                return redirect('/article-1-%s.html'%(cate_id))
            else:
                return render(request,'login.html',{'obj':obj})
        else:
            return render(request,'login.html',{'obj':obj})

def logout(request):
    request.session.clear()

    return redirect('/')

@csrf_exempt
def register(request):
    msg=''
    if request.method=='GET':
        obj=Fm()
        return render(request,'register.html',{'obj':obj,'msg':msg})
    elif request.method=='POST':
        obj=Fm(request.POST)
        ob_1=obj.is_valid()
        if ob_1:
            u=request.POST.get('user')
            p=request.POST.get('pwd')
            test_u=models.UserInfo.objects.filter(username=u)
            if test_u:
                msg='用户名已经存在'
                return render(request,'register.html',{'obj':obj,'mag':msg})
            else:
                models.UserInfo.objects.create(username=u,password=p)
                request.session['user']=u
                request.session['is_login']=True
                u_id=models.UserInfo.objects.filter(username=u).first().nid
                models.Cate.objects.create(caption=u,user_id=u_id)
                cate_id=models.Cate.objects.filter(caption=u).first().id
                return redirect('/article-1-%s.html'%(cate_id))
        else:
            return render(request,'register.html',{'obj':obj,'msg':msg})

@csrf_exempt
def add_article(request):
    if request.session.get('is_login',None):
        user = request.session['user']
        cate_id=models.UserInfo.objects.filter(username=user).first().cate.id
        if request.method == 'GET':
            form = ArticleForm(request=request)
            return render(request,'add_article.html',{'form': form,'cate_id':cate_id})
        elif request.method == 'POST':
            form = ArticleForm(request=request, data=request.POST)
            if form.is_valid():
                with transaction.atomic():
                    content = form.cleaned_data.pop('content')
                    form.cleaned_data['content'] = content
                    user = request.session['user']
                    cate_id=models.UserInfo.objects.filter(username=user).first().cate.id
                    form.cleaned_data['cate_id'] = cate_id
                    print(form.cleaned_data)
                    obj = models.Articl.objects.create(**form.cleaned_data)
                return redirect('/article-1-%s.html'%(cate_id))
            else:
                return render(request, 'add_article.html', {'form': form,'cate_id':cate_id})
        else:
                return redirect('/')
    else:
        return HttpResponse("请先登陆")


