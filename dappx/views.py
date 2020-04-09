
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import UserProfileInfo, Question, Choice
from django.utils import timezone
from django.views import generic


# Create your views here.

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('dappx:index'))

#@method_decorator(login_required)
class IndexView(View):
    template_name = 'dappx/index.html'  # the template to load through this view

    def get(self, request, *args, **kwargs):



            latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

            return render(request, self.template_name, {'latest_question_list': latest_question_list})




class DetailView(generic.DetailView):
    model = Question
    template_name = 'dappx/detail.html'
    context_object_name = 'question'



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'dappx/result.html'
    context_object_name = 'question'





def vote(request,question_id):
    if(request.method == "POST"):
        question = Question.objects.get(pk = question_id)
        try:
            selected_choice = question.choice_set.get(pk = request.POST['choice'])
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'dappx/detail.html',
                          {'question': question, 'error_message': "you didn't select a choice", })
        else:
            selected_choice.vote += 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('dappx:results', args = (question.id,)))







class RegisterView(View):
    user_form = UserForm
    template_name = 'dappx/registration.html'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form()
        return render(request, self.template_name,{'user_form':user_form,})


    def post(self, request, *args, **kwargs):

        registered = False
        user_form = self.user_form(request.POST)


        if(user_form.is_valid):
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)

        return render(request,self.template_name,{'registered':registered, 'user_form':user_form,})



class LoginView(View):
    template_name = 'dappx/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self,request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username= username, password= password)
        #user1 = UserProfileInfo.objects.filter(name=username, password=password)

        if(user):
            if(user.is_active):
                login(request,user)
                return HttpResponseRedirect(reverse('dappx:index'))
            else:
                return HttpResponse("Your account was inactive.")

        else:
            return HttpResponse("Someone tried to login and failed. They used username: {} and password: {}".format(username,password))
