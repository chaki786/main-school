from django.urls import path
from . import views
from .views import DashboardView, AcceptFollowRequestView, DeleteThread, DeleteMessageView, Manage_principal, EditProfile, PhotoDeleteView, ProfileView,PhotoDetailView, PhotoListView,RatingChartView,PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, AddLike, AddDislike, AddCommentLike, AddCommentDislike, CommentReplyView, PostNotification, FollowNotification, RemoveNotification, SharedPostView,ListFollowers,AddFollower,ListThreads,CreateThread,CreateMessage,ThreadView,ThreadNotification

app_name= 'hod'

urlpatterns = [
    path('menu/',views.menu,name='menu'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('create/', views.school_create, name='school_create'),
    path('edit/<int:school_id>', views.school_edit, name='school_edit'),
    path('delete_about/<int:school_id>', views.school_delete, name='delete_about'),
    path('about/<int:about_id>/', views.school_detail, name='school_detail'),

    path('add_principal/',views.add_principal,name="add_principal"),
    path('manage-principal/<int:principal_id>/', views.manage_principal, name='manage_principal'),
    path('manage-principals/<int:principal_id>/', views.manage_principals, name='manage_principals'),
    path('edit_principal/<str:principal_id>', views.edit_principal,name="edit_principal"),
    path('delete_form/<str:pk>', views.deleteform,name="deleteform"),

    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile'),

    path('profile/<int:pk>/', Manage_principal.as_view(), name='profiles'),
    path('editprofile/', EditProfile.as_view(), name='edit_profile'),

    path('dashboardfollow/', DashboardView.as_view(), name='dashboardfollow'),
    path('follow-requests/<int:pk>/accept/', AcceptFollowRequestView.as_view(), name='accept_follow_request'),
    path('profiles/<int:pk>/follow/', views.FollowProfile.as_view(), name='follow_profile'),
    path('profiles/<int:pk>/unfollow/', views.UnfollowProfile.as_view(), name='unfollow_profile'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),
    path('profile/<int:pk>/followers/add/', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/<int:follower_pk>/unfollow/', views.UnfollowFollower.as_view(), name='unfollow_follower'),

    path('post',PostListView.as_view(),name='post_list'),
    path('post_detail/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('post_edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post/<int:pk>/share', SharedPostView.as_view(), name='share-post'),

    path('post/<int:post_pk>/comment/<int:comment_pk>/edit/', views.edit_comment, name='comment_edit'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    
    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('follow-notification/<int:notification_pk>/<int:profile_pk>/', FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
    path('notification/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('delete-thread/<int:pk>/', DeleteThread.as_view(), name='delete-thread'),
    path('message/delete/<int:pk>/', DeleteMessageView.as_view(), name='delete-message'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),

    path('photos/',PhotoListView.as_view(),name='photo'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('rating',RatingChartView.as_view(),name='rating'),
]