from django.test import TestCase, Client
from django.test.utils import setup_test_environment, teardown_test_environment
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm
from django.urls import reverse


class PostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.testData = [ {'title':'lafdk0', 'text':'book'},
                {'title':'', 'text':'book'}]
           


    def testFormEmpty(self):
        form = PostForm(data=self.testData[1])
        self.assertFalse(form.is_valid())

    def testForm(self):
        form = PostForm(data=self.testData[0])
        self.assertTrue(form.is_valid())
        user = User.objects.create_user('john', 'johndoe@test.com', 'doe')
        self.client.login(username='john', password='doe')
        for book in self.testData:
            response = self.client.post("/post/new/", {'user':user, 'title':book['title'], 'text':book['text']})

    def testIndex(self):
        try:
	        teardown_test_environment()
        except AttributeError:
            pass
        setup_test_environment()
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.context['posts'], Post.objects.filter(text='book'))
