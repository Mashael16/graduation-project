from ..models import Task, Evaluation

def get_dashboard_summary(user):

    if user.role == 'employee':
        total_tasks = Task.objects.filter(
            assigned_to=user
        ).count()

        completed_tasks = Task.objects.filter(
            assigned_to=user,
            status='completed'
        ).count()

        evaluations = Evaluation.objects.filter(
            task__assigned_to=user
        ).count()

    else:
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(
            status='completed'
        ).count()
        evaluations = Evaluation.objects.count()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "evaluations": evaluations
    }
