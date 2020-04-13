from django.test import TestCase, Client
from django.utils import timezone
import datetime
from .models import Question,Choice
from django.urls import reverse, resolve
from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_login_view_authenticated_user(self):
        res = self.client.get(reverse('dappx:user_login'))
        self.assertEquals(res.status_code,200)
        self.username = 'nitikesh'
        self.password = '123'
        user = User.objects.create(username = self.username)
        user.set_password(self.password)
        user.save()
        res = self.client.post(reverse('dappx:user_login'), {'username':'nitikesh', 'password':'123'})
        self.assertEqual(res.status_code,302)
        res = self.client.get(reverse('dappx:index'))
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res, 'dappx/index.html')

    def test_login_view_unauthenticated_user(self):
        res = self.client.get(reverse('dappx:user_login'))
        self.assertEqual(res.status_code,200)
        self.assertTrue(b'Login' in res.content)
        res = self.client.post(reverse('dappx:user_login'),{'username':'nitikesh', 'password':'123'})
        self.assertEqual(res.status_code,200)




class LogoutView(TestCase):
    def setUp(self):
        self.client = Client()
    def test_logout_view(self):
        self.username = 'nitikesh'
        self.password = '123'
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        res = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})
        self.assertEqual(res.status_code,302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTrue(b'Logout' in res.content)
        self.client.logout()
        res = self.client.get(reverse('logout'))
        self.assertEqual(res.status_code,302)
        res = self.client.get(reverse('dappx:index'))
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res, 'dappx/index.html')


class ModelTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Question_model(self):
        q = Question(question_text= 'hi there')
        self.assertEqual(str(q),q.question_text)

    def test_Choice_model(self):
        c = Choice(choice_text = 'funny_text')
        self.assertEqual(str(c), c.choice_text)



def create_question(question_text, days):     #func is used to create questions with their respective parameters whenever they are called
    time = timezone.now() + datetime.timedelta(days = days)    #creates time based on parameter passed
    return Question.objects.create(question_text = question_text,pub_date = time)   #sends Question object with respective question_text and publish date

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
        q = create_question(question_text= 'question is here', days = -2)
        c = q.choice_set.create(choice_text = 'hello')
        q1 = Question.objects.get(pk = q.id)
        c1 = q1.choice_set.get(pk = c.id)
        res = self.client.post(reverse('dappx:vote', args = (q1.id,)), {'choice':c1.id})
        self.assertEqual(res.status_code,302)


    def test_vote_view_no_choice(self):
        q = create_question(question_text='question is here', days=-2)
        c = q.choice_set.create(choice_text="hello")
        x = Question.objects.get(pk = q.id)
        y = x.choice_set.get(pk = c.id)
        response = self.client.post(reverse('dappx:vote', args=(x.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dappx/detail.html')



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










class QuestionIndexViewTests(TestCase):



    def setUp(self):
        self.client = Client()
        self.quest_url = reverse('dappx:user_login')
        self.username = 'nitikesh'
        self.password = '123'
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()


    def test_future_and_past_question(self):
        create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)


        res = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})

        self.assertEqual(res.status_code,302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTemplateUsed(res, 'dappx/index.html')
        self.assertEqual(res.status_code,200)
        self.assertQuerysetEqual(res.context['latest_question_list'], ['<Question: Past question>'])



    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})
        self.assertEqual(response.status_code,302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTemplateUsed(res, 'dappx/index.html')
        self.assertQuerysetEqual(res.context['latest_question_list'], [])







    def test_no_question(self):  # checks the message: "No polls are available" and verifies the latest_question_list is empty. It doesn't create any questions.
        response = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})
        self.assertEqual(response.status_code, 302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTemplateUsed(res, 'dappx/index.html')
        self.assertQuerysetEqual(res.context['latest_question_list'], [])  # asserts that query set(1st parameter) returns second parameter list of views.

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})
        self.assertEqual(response.status_code, 302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTemplateUsed(res, 'dappx/index.html')
        self.assertQuerysetEqual(res.context['latest_question_list'], ['<Question: Past question.>'])



    def test_two_past_questions(self):
        create_question(question_text="past question 1.", days=-30)
        create_question(question_text="past question 2.", days=-5)
        response = self.client.post(reverse('dappx:user_login'), {'username': 'nitikesh', 'password': '123'})
        self.assertEqual(response.status_code, 302)
        res = self.client.get(reverse('dappx:index'))
        self.assertTemplateUsed(res, 'dappx/index.html')
        self.assertQuerysetEqual(res.context['latest_question_list'], ['<Question: past question 2.>', '<Question: past question 1.>'])


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



class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        res = self.client.get(reverse('dappx:register'))
        self.assertEquals(res.status_code,200)
        self.assertTemplateUsed(res, 'dappx/registration.html')
        res = self.client.post(reverse('dappx:register'), data = {'username':'abhishek', 'password':123,
                                                                  'email':'abhishek@gmail.com'})
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res, 'dappx/registration.html')


class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_detail_url_is_resolved(self):
        url = reverse('dappx:detail', args =[1])
        print(resolve(url).func)



    def test_index_url_is_resolved(self):
        url = reverse('dappx:index')
        print(resolve(url).func)  #resolve() method takes a URL as a string and returns a ResolverMatch object which provides access to all attributes  of the resolved URL match.



    def test_result_url_is_resolve(self):
        url = reverse('dappx:results', args = [1])
        print(resolve(url).func)




    def test_vote_url_is_resolve(self):
        url = reverse('dappx:vote', kwargs = {'question_id': 1})
        print(resolve(url).func)
        
        
        
