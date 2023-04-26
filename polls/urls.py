from django.urls import path
from . import views
from .views import FollowToggle,FollowToggles,FollowTogglet,ListFollowers,ListFollowerss,ListFollowerst, HomeView,Menus,PhotoDetailView,RatingChartView,PhotoListView,PostDetailView,PostListView
from .viewsauth import PasswordResetDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView

app_name= 'polls'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('menu/<int:school_id>/', views.Menu.as_view(), name='menu'),
    path('Menus',Menus.as_view(),name='menus'),
    path('addschool/', views.add_school,name="addschool"),

    path('manage-principal/<int:principal_id>/', views.manage_principal, name='manage_principal'),
    path('manage-principals/<int:principal_id>/', views.manage_principals, name='manage_principals'),
    path('manage_teacher/<int:principal_id>/', views.manage_teacher, name='manage_teacher'),
    path('manage_student/<int:principal_id>/', views.manage_student,name="manage_student"),

    path('Student_Register/',views.studentreg,name="student_reg"),
    path('pal',views.principalreg,name="principal_reg"),
    path('Teacher_Register',views.teacherreg,name="teacher_reg"),

    path('Login',views.loginn,name="loginn"),
    path('Logout',views.logouts,name="logout"),
    
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('post',PostListView.as_view(),name='post_list'),
    path('post_detail/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('photos/<int:school_id>/',PhotoListView.as_view(),name='photo'),
    path('photosdetail/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('rating/<int:school_id>/', RatingChartView.as_view(), name='rating'),

    path('profiles_principal/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),
    path('<int:pk>/follow-toggle/', FollowToggle.as_view(), name='follow_toggle'),

    path('profiles_teacher/<int:pk>/followers/', ListFollowerst.as_view(), name='list-followerst'),
    path('teacher/<int:pk>/follow-toggle/', FollowTogglet.as_view(), name='follow_togglet'),

    path('profiles_student/<int:pk>/followers/', ListFollowerss.as_view(), name='list-followerss'),
    path('student/<int:pk>/follow-toggle/', FollowToggles.as_view(), name='follow_toggles'),

]