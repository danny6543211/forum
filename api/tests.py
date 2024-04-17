from django.test import TestCase
import requests

# Create your tests here.
class InitTestCase(TestCase):
    def setUp(self):
        # user1
        requests.post('http://127.0.0.1:8000/api/user/register/', data={
            'username': '2020056086',
            'password': 'Da901128@@',
            'nickname': 'danny',
        })
        # user2
        requests.post('http://127.0.0.1:8000/api/user/register/', data={
            'username': '2020012345',
            'password': 'Da901128@@',
            'nickname': 'merry',
        })

        user1_login_response = requests.post('http://127.0.0.1:8000/api/user/login/', data={
            'username': '2020056086',
            'password': 'Da901128@@',
        })
        user2_login_response = requests.post('http://127.0.0.1:8000/api/user/login/', data={
            'username': '2020012345',
            'password': 'Da901128@@',
        })
        user1_token = 'Token ' + user1_login_response.json()['token']
        user2_token = 'Token ' + user2_login_response.json()['token']
        
        # user1 profile setting
        requests.put('http://127.0.0.1:8000/api/profile/1/', data={
            'user': '1',
            'nickname': 'danny',
            'bio': 'I\'m student.',
            'birthday': '2001-11-28',
            'gender': 'male',
        }, headers={'Authorization': user1_token})
        # user2 profile setting
        requests.put('http://127.0.0.1:8000/api/profile/2/', data={
            'user': '2',
            'nickname': 'merry',
            'bio': 'I\'m student.',
            'birthday': '2001-9-6',
            'gender': 'female',
        }, headers={'Authorization': user2_token})

        # article1 created by user1
        requests.post('http://127.0.0.1:8000/api/article/', data={
            'user': '1',
            'title': 'Test article title created by user1',
            'content': 'Test article content created by user1'
        }, headers={'Authorization': user1_token})
        # article2 created by user2
        requests.post('http://127.0.0.1:8000/api/article/', data={
            'user': '2',
            'title': 'Test article title created by user2',
            'content': 'Test article content created by user2'
        }, headers={'Authorization': user2_token})
        
        # comment article2 by user1
        requests.post('http://127.0.0.1:8000/api/comment/', data={
            'user': '1',
            'article': '2',
            'content': 'hello user2'
        }, headers={'Authorization': user1_token})

        # comment article1 by user2
        requests.post('http://127.0.0.1:8000/api/comment/', data={
            'user': '2',
            'article': '1',
            'content': 'hello user1'
        }, headers={'Authorization': user2_token})

    def test_article_comment(self):
        response = requests.post('http://127.0.0.1:8000/api/article/comments/', data={
            'article': '1'
        })

        print(response.json())