from django.test import TestCase
from django.urls import reverse
from .models import Question
from django.utils import timezone
import  datetime
# Create your tests here.

class QuestionModelTest(TestCase):

    def test_was_publish_recently_with_future_qeustion(self):
        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date = time)

        self.assertIs(question.was_publish_recently(), False)

    def test_was_publish_recently_with_recently_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(pub_date=time)

        self.assertIs(question.was_publish_recently(), True)

    def test_was_publish_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=time)

        self.assertIs(question.was_publish_recently(), False)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question>'])

    def test_future_question(self):
        create_question(question_text='Fulture question', days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No Polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_fulture_and_past_question(self):
        '''
        check past question and fulture qeustion
        :return:
        '''
        create_question(question_text='Past question', days=-10)
        create_question(question_text='Fulture question', days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_two_past_question(self):
        create_question(question_text='Past question 1', days=-10)
        create_question(question_text='Past question 2', days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 1>','<Question: Past question 2>'])

class QuestionDetailViewTest(TestCase):
    def test_fulture_question(self):
        fulture_question = create_question(question_text='fulture question', days=10)
        url = reverse('polls:detail', args=(fulture_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)

def create_question(question_text, days):
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
