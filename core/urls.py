from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet,EvaluationViewSet,TaskEvaluation,MyTasksView,MyEvaluationsView,DashboardSummaryView



router = DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('evaluations', EvaluationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:task_id>/evaluation/', TaskEvaluation.as_view()),
    path('my-tasks/', MyTasksView.as_view()),
    path('my-evaluations/', MyEvaluationsView.as_view()),
    path('dashboard-summary/', DashboardSummaryView.as_view()),

]