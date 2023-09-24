from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.conf import settings

User = get_user_model()





class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name='courses_enrolled', blank=True)
    
    def __str__(self):
        return self.user.username

    
    

class Course(models.Model):
    name = models.CharField(max_length=200)
    # student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.IntegerField()
    description = models.TextField()
    price = models.FloatField()

    what_you_will_learn = models.CharField(max_length=2000)
    duration = models.DurationField()
    students = models.ManyToManyField(User, through='Enrollment')

    COURSE_LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    course_level = models.CharField(
        max_length=20,
        choices=COURSE_LEVEL_CHOICES,
        default='beginner',
    )
    course_video = CloudinaryField("Course Video")
    course_image = CloudinaryField("Course Image")
    
    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.name} on {self.enrollment_date}'

    

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField()
    number_of_lessons = models.PositiveIntegerField(default=0)
    number_of_labs = models.PositiveIntegerField(default=0)
    number_of_quizzes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.topic
    

class Lesson(models.Model):
    lesson = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField()
   

    def __str__(self):
        return self.lesson
    

class Quiz(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.DurationField()
    pass_percentage = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Lab(models.Model):
    lab_name= models.ForeignKey(Topic, on_delete=models.CASCADE)
    task = models.TextField()
    topic_id = models.IntegerField()

    def __str__(self):
        return self.lab_name
    

class CourseDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_reviews = models.IntegerField()
    num_students = models.IntegerField()
    avg_rating = models.FloatField()
    num_topics = models.IntegerField()
    num_quizzes = models.IntegerField()
    num_labs = models.IntegerField()



class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user


    
class Progress(models.Model):
    # student = models.OneToOneField('Student', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)




class Question(models.Model):
    text = models.TextField()
    # Any other fields needed for your questions
    
    def __str__(self):
        return self.text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text        
    



class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)




class LabTaskSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    labtask = models.ForeignKey(Lab, on_delete=models.CASCADE,)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.lab.title}"


class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.lesson.title}"


class TopicCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.topic.title}"