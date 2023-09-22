from django.contrib import admin
from .models import Course,Topic,Lesson,Quiz,Lab,Student,CourseDetail,Review,Progress,Question,Choice,Answer,QuizSubmission,LabTaskSubmission,LessonCompletion,TopicCompletion

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Lab)
admin.site.register(Student)
admin.site.register(CourseDetail)
admin.site.register(Review)
admin.site.register(Progress)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(QuizSubmission)
admin.site.register(LabTaskSubmission)
admin.site.register(LessonCompletion)
admin.site.register(TopicCompletion)