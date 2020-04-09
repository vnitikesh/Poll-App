from django.test import TestCase, Client
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse, resolve
from .views import IndexView, DetailView, vote, ResultsView
from . import views


class QuestionClassResultVoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_result_view(self):
        q = create_question(question_text='question is here', days=-2)
        c = q.choice_set.create(choice_text="hello")
        response = self.client.get(reverse('dappx:results', args=(c.id,)))

        self.assertTemplateUsed(response, 'dappx/result.html')
        self.assertEqual(response.status_code, 200)

    def test_vote_view(self):
        q = create_question(question_text='question is here', days=-2)
        c = q.choice_set.create(choice_text="hello")
        response = self.client.post(reverse('dappx:vote', args=(c.id,)))
        self.assertEqual(response.status_code, 200)


class QuestionDetailViewTests(TestCase):



    def setUp(self):
        self.client = Client()



    def test_past_question(self):
        past_question = create_question(question_text = 'Past question.', days = -30)
        past_choice = past_question.choice_set.create(choice_text = "hi")
        url = reverse("dappx:detail", args = (past_choice.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)
        self.assertTemplateUsed(response,'dappx/detail.html')



def create_question(question_text, days):     #func is used to create questions with their respective parameters whenever they are called
    time = timezone.now() + datetime.timedelta(days = days)    #creates time based on parameter passed
    return Question.objects.create(question_text = question_text,pub_date = time)   #sends Question object with respective question_text and publish date





class QuestionIndexViewTests(TestCase):

    # database is reset for each test method, so the first question is no longer there.

    def setUp(self):
        self.client = Client()
        self.quest_url = reverse('dappx:user_login')


    def test_future_and_past_question(self):
        create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(self.quest_url)
        #print(response.status_code)
        self.assertTemplateUsed(response, 'dappx/login.html')
        #self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])


    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(self.quest_url)
        print(response.status_code)
        self.assertTemplateUsed(response, 'dappx/login.html')
        self.assertContains(response, "No polls are available.", count=0)
        #self.assertQuerysetEqual(response.context['latest_question_list'], [])







    def test_no_question(self):  # checks the message: "No polls are available" and verifies the latest_question_list is empty. It doesn't create any questions.
        response = self.client.get(self.quest_url)
        self.assertEqual(response.status_code, 200)  # asserts that response.status_code == 200
        self.assertContains(response, "No polls are available", count=0)  # text appears in the content of the given response instance
        self.assertTemplateUsed(response, 'dappx/login.html')
        #self.assertQuerysetEqual(response.context['latest_question_list'], [])  # asserts that query set(1st parameter) returns second parameter list of views.

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(self.quest_url)

        self.assertTemplateUsed(response, 'dappx/login.html')
        #self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])



    def test_two_past_questions(self):
        create_question(question_text="past question 1.", days=-30)
        create_question(question_text="past question 2.", days=-5)
        response = self.client.get(self.quest_url)

        self.assertTemplateUsed(response, 'dappx/login.html')
        #self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question 2.>', '<Question: past question 1.>'])


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days = 1,seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(),True)














class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_detail_url_is_resolved(self):
        url = reverse('dappx:detail', args =[1])
        print(resolve(url).func)
        #print("\n")
        #self.assertEquals(resolve(url).func,DetailView.as_view())


    def test_index_url_is_resolved(self):
        url = reverse('dappx:index')
        print(resolve(url).func)  #resolve() method takes a URL as a string and returns a ResolverMatch object which provides access to all attributes  of the resolved URL match.
        #print('\n')
        #self.assertEquals(resolve(url).func, IndexView())


    def test_result_url_is_resolve(self):
        url = reverse('dappx:results', args = [1])
        print(resolve(url).func)
        print(ResultsView.as_view())
        #print("\n")
        #self.assertEquals(resolve(url).func,ResultsView.as_view())



    def test_vote_url_is_resolve(self):
        url = reverse('dappx:vote', kwargs = {'question_id': 1})
        print(resolve(url).func)
        #print("\n")
        #self.assertEquals(resolve(url).func, vote)





