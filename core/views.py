# This code defines a ViewSet, which is a high-level component that automatically handles the logic for standard CRUD operations (Create, Retrieve, Update, Delete)
#  by combining a data source (queryset) with a translator (serializer_class),
# effectively creating all the necessary API endpoints for the Task model in just a few lines of code.


from rest_framework import viewsets,permissions
from .models import Task,Evaluation
from .serializers import TaskSerializer ,EvaluationSerializer
from .permissions import IsManager
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Count
from .services.dashboard_service import get_dashboard_summary
from .services.evaluation_service import create_evaluation



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        if self.request.role != 'manager':
            raise PermissionDenied("only managers can assign tasks")
        serializer.save()

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

# from .serializers import GamificationSerializer
# class GamificationViewSet(viewsets.ModelViewSet):
#     queryset = Gamification.objects.all()
#     serializer_class = GamificationSerializer



# class TaskEvaluationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, task_id):
#         evaluation = Evaluation.objects.get(task_id=task_id)
#         serializer = EvaluationSerializer(evaluation)
#         return Response(serializer.data)

#     def post(self, request, task_id):
#         serializer = EvaluationSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(
#                 task_id=task_id,
#                 evaluator=request.user
#             )
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)

class TaskEvaluation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user.role == 'employee':
            if task.assigned_to != request.user:
                return Response(
                    {"error": "You can only view your own evaluations"},
                    status=status.HTTP_403_FORBIDDEN
                )

        evaluation = get_object_or_404(Evaluation, task=task)
        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data)

    def post(self, request, task_id):

        if request.user.role != 'manager':
            return Response(
                {"error": "Only managers can create evaluations"},
                status=403
            )

        data, error = create_evaluation(
        task_id=task_id,
        user=request.user,
        data=request.data,
        serializer_class=EvaluationSerializer
    )
        
        if error:
            return Response({"error": error}, status=400)

        return Response(data, status=201)
        


class MyTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == 'employee':
            tasks = Task.objects.filter(assigned_to=request.user)

        else: 
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class MyEvaluationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == 'employee':
            evaluations = Evaluation.objects.filter(
                task__assigned_to=request.user
            )
        else:  
            evaluations = Evaluation.objects.all()

        serializer = EvaluationSerializer(evaluations, many=True)
        return Response(serializer.data)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_dashboard_summary(request.user)
        return Response(data)