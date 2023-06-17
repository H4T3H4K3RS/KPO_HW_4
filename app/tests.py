from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task


class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_task(self):
        """
        Test creating a new task.
        """
        url = reverse('task-list')
        data = {'title': 'New Task', 'description': 'Task description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'New Task')

    def test_get_task_list(self):
        """
        Test retrieving a list of tasks.
        """
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_detail(self):
        """
        Test retrieving a specific task.
        """
        task = Task.objects.create(title='Test Task', description='Task description')
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        """
        Test partially updating a task using PATCH.
        """
        task = Task.objects.create(title='Test Task', description='Task description')
        url = reverse('task-detail', kwargs={'pk': task.pk})
        data = {'title': 'Updated Task'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get().title, 'Updated Task')

    def test_delete_task(self):
        task = Task.objects.create(title='Test Task', description='Task description')
        url = reverse('task-detail', kwargs={'pk': task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_with_invalid_pk(self):
        url = reverse('task-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_with_invalid_data(self):
        """
        Test creating a new task with invalid data.
        """
        url = reverse('task-list')
        invalid_data = {'description': 'Task description'}  # Missing 'title' field
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_with_invalid_data(self):
        task = Task.objects.create(title='Test Task', description='Task description')
        url = reverse('task-detail', kwargs={'pk': task.pk})
        invalid_data = {'title': ''}
        response = self.client.put(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
