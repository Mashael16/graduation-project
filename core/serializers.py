# This code defines a TaskSerializer that acts as a bridge between your Django models and the JSON format;
#  it uses ModelSerializer to automatically map all fields (__all__) from the Task model into a format 
# that can be easily parsed by frontend applications (like React or Mobile apps) while also handling data validation when saving new entries.

from rest_framework import serializers
from .models import Task, User ,Evaluation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

# from .models import Gamification
# class GamificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gamification
#         fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['task']