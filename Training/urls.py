from django.urls import path, include
from .views import(UserViewset,CourseAdminViewSet,TopicAdminViewSet,LessonAdminViewSet,QuizAdminViewSet,CourseDetailAdminViewSet,LabAdminViewSet,ReviewAdminViewSet,UserCourseViewSet,CourseDetailViewSet,
                    EnrollmentViewSet,StartCourseViewSet,ProgressViewSet,EnrolledCoursesViewSet,ReviewViewSet,CourseContentsViewSet,QuizSubmissionViewSet,LabTaskSubmissionViewSet,LessonCompletionViewSet,TopicCompletionViewSet)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router =DefaultRouter()
router.register(r'admin/courses', CourseAdminViewSet)
router.register(r'admin/topics', TopicAdminViewSet)
router.register(r'admin/lessons', LessonAdminViewSet)
router.register(r'admin/quizes', QuizAdminViewSet)
router.register(r'admin/lab', LabAdminViewSet)
router.register(r'admin/review', ReviewAdminViewSet)
router.register(r'admin/course-details', CourseDetailAdminViewSet)
router.register(r'courses', UserCourseViewSet, basename='user-course')
router.register(r'course-details', CourseDetailViewSet, basename='course-detail')
router.register(r'enroll', EnrollmentViewSet, basename='enroll')
router.register(r'start-course', StartCourseViewSet, basename='start-course')
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(r'enrolled-courses', EnrolledCoursesViewSet, basename='enrolled-courses')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'courses', CourseContentsViewSet, basename='courses')
router.register(r'quiz-submissions', QuizSubmissionViewSet, basename='quiz-submissions')
router.register(r'lab-task-submissions', LabTaskSubmissionViewSet, basename='lab-task-submissions')
router.register(r'lesson-completions', LessonCompletionViewSet, basename='lesson-completions')
router.register(r'topic-completions', TopicCompletionViewSet, basename='topic-completions')
router.register(r'users', UserViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('start-course/<int:pk>/', StartCourseViewSet.as_view({'get': 'get_started_course'}), name='get-started-course'),
    path('courses/<int:course_pk>/topics/<int:topic_pk>/', include(router.urls)),

]



