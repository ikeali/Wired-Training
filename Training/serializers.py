from .models import (Course,Enrollment,Topic,Lesson,Quiz,Lab,Review,CourseDetail,Student,Progress,Answer, QuizSubmission,LabTaskSubmission,LessonCompletion,TopicCompletion)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =Review
        fields = '__all__'


class ContentSerializer(serializers.Serializer):
    lesson = LessonSerializer(many=True)
    quiz = QuizSerializer(many=True)
    lab = LabSerializer(many=True)



class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = '__all__'

class StartCourseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    course_id = serializers.IntegerField()

    def create(self, validated_data):
        email = validated_data['email']
        course_id = validated_data['course_id']
        
        # User = get_user_model()

        user = User.objects.get(email=email)

        try:
            student = user.student
        except Student.DoesNotExist:
            student = Student.objects.create(user=user)
        
        course = Course.objects.get(pk=course_id)
        student.courses.add(course)
        
        return student
    
    
        

class EnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class QuizSubmissionSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True)

    class Meta:
        model = QuizSubmission
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'selected_choice']




class LabTaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTaskSubmission
        fields = '__all__'


class LessonCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonCompletion
        fields = ['lesson']

class TopicCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicCompletion
        fields = ['topic']