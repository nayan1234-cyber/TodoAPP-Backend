from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ToDo.models import TODO


class ToDoListTest(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Create To-Do items for each user
        self.todo1 = TODO.objects.create(title="Task 1", status="0", priority="1", user=self.user1)
        self.todo2 = TODO.objects.create(title="Task 2", status="1", priority="2", user=self.user1)
        self.todo3 = TODO.objects.create(title="Task 3", status="0", priority="1", user=self.user2)

        # URL for ToDo list view
        self.url = reverse('todo-list')  # Adjust the URL name if needed

    def test_authenticated_user_can_see_own_todos(self):
        # Login and get the JWT token
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'user1', 'password': 'password123'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # Use the token for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('todo-list'))

        # Check for the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # user1 should have 2 todos

    def test_unauthenticated_user_cannot_access_todos(self):
        # Send request without authentication token
        response = self.client.get(reverse('todo-list'))

        # Check for Unauthorized response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_authenticated_user_can_create_todo(self):
    # Login and get the JWT token
    response = self.client.post(reverse('token_obtain_pair'), data={'username': 'user1', 'password': 'password123'},
                                format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    token = response.data['access']

    # Create a ToDo with the token in the Authorization header
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    todo_data = {'title': 'New Task', 'status': '0', 'priority': '1'}
    response = self.client.post(reverse('todo-list'), data=todo_data, format='json')

    # Check for a successful response
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

