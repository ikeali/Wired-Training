from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.decorators import action
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .models import Course,Topic,Lesson,Quiz,Lab,Review,CourseDetail,Student,Progress,QuizSubmission,LabTaskSubmission,LessonCompletion,TopicCompletion
from .serializers import (UserSerializer,CourseSerializer,TopicSerializer,LessonSerializer,QuizSerializer,LabSerializer,ReviewSerializer,CourseDetailSerializer,StartCourseSerializer,ProgressSerializer,EnrolledCourseSerializer,ContentSerializer,QuizSubmissionSerializer, LabTaskSubmissionSerializer,LessonCompletionSerializer,TopicCompletionSerializer)
from rest_framework.decorators import action

User = get_user_model()

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['post'])
    def signin(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
   
        if username is None or password is None:
            return Response({'error': 'Both username and password are required.'}, status=400)

        user = authenticate(username=username, password=password)
        print("Authenticated user:", user)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            print("Token key:", token.key)

            return Response({'token': token.key}, status=200)
        else:
            return Response({'error': 'Invalid username or password.'}, status=400)


class CourseAdminViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]
   

class TopicAdminViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]



class LessonAdminViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]



class QuizAdminViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAdminUser]


class LabAdminViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [IsAdminUser]


class ReviewAdminViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]

class CourseDetailAdminViewSet(viewsets.ModelViewSet):
    queryset = CourseDetail.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAdminUser]


    def approve_review(self, request, pk=None):
        review = self.get_object()
        review.is_approved = True
        review.save()
        return Response({"message": "Review approved"}, status=status.HTTP_200_OK)


class UserCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny] 



class CourseDetailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseDetailSerializer

    def get_queryset(self):
        return CourseDetail.objects.all()

    @action(detail=True, methods=['get'])
    def course_stats(self, request, pk=None):
        course = self.get_object()
        num_reviews = course.reviews.count()
        num_students = course.enrollments.count()
        avg_rating = course.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        num_topics = course.topics.count()
        num_quizzes = course.quizzes.count()
        num_labs = course.labs.count()

        stats_data = {
            'num_reviews': num_reviews,
            'num_students': num_students,
            'avg_rating': avg_rating,
            'num_topics': num_topics,
            'num_quizzes': num_quizzes,
            'num_labs': num_labs,
        }

        return Response(stats_data)


class StartCourseViewSet(viewsets.ViewSet):
    serializer_class = StartCourseSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.create(serializer.validated_data)
        
        return Response({
            'message': 'Course started successfully.',
            'student_id': student.id,
            'course_id': serializer.validated_data['course_id']
        }, status=201)

    
    def get_started_course(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data)
    

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]
    queryset = Progress.objects.all()

    @action(detail=True, methods=['POST'])
    def mark_topic_completed(self, request, pk=None):
        student = request.user.student
        topic = get_object_or_404(Topic, id=pk)
        
        # Create or update progress entry for the completed topic
        progress_entry, created = Progress.objects.get_or_create(
            student=student,
            course=topic.course,
            topic=topic,
            defaults={'completed': True}
        )
        
        if not created:
            progress_entry.completed = True
            progress_entry.save()
        
        # Update course progress for the associated student
        self.update_course_progress(student, topic.course)
        
        return Response({'message': 'Topic marked as completed.'}, status=status.HTTP_200_OK)
    
    def update_course_progress(self, student, course):
        topics_in_course = course.topic_set.all()
        completed_topics = Progress.objects.filter(student=student, topic__in=topics_in_course, completed=True)
        total_topics = topics_in_course.count()
        completed_topic_count = completed_topics.count()
        
        course_progress_percentage = (completed_topic_count / total_topics) * 100
        
        # Update the course progress for the student
        student.courses.through.objects.filter(student=student, course=course).update(progress=course_progress_percentage)

    

class EnrolledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        try:
            student = user.student
        except Student.DoesNotExist:
            return Course.objects.none()  # Return empty queryset if user has no student profile
        
        enrolled_courses = student.courses.all()
        return enrolled_courses  
     

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)    
    

class CourseContentsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer  # Use the appropriate serializer for the topic

    def retrieve(self, request, *args, **kwargs):
        topic = self.get_object()
        user = request.user

        lesson_contents = Lesson.objects.filter(topic=topic)
        quiz_contents = Quiz.objects.filter(topic=topic)
        lab_contents = Lab.objects.filter(topic=topic)

        lesson_serializer = LessonSerializer(lesson_contents, many=True)
        quiz_serializer = QuizSerializer(quiz_contents, many=True)
        lab_serializer = LabSerializer(lab_contents, many=True)

        topic_data = {
            'title': topic.title,
            'lessons': lesson_serializer.data,
            'quizzes': quiz_serializer.data,
            'labs': lab_serializer.data
        }

        # Serialize the topic data using the specified serializer
        serializer = self.get_serializer(topic_data)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return Topic.objects.filter(course__students=user)
    

class QuizSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return QuizSubmission.objects.filter(user=user)   


class LabTaskSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = LabTaskSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return LabTaskSubmission.objects.filter(user=user)


class LessonCompletionViewSet(viewsets.ModelViewSet):
    serializer_class = LessonCompletionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return LessonCompletion.objects.filter(user=user)
    

class TopicCompletionViewSet(viewsets.ModelViewSet):
    serializer_class = TopicCompletionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return TopicCompletion.objects.filter(user=user)    
  