from rest_framework import status, viewsets
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return self.serializer_class

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
