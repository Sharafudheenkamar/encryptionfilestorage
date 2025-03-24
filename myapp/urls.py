from django.urls import path
from .views import *

urlpatterns = [
    path('',Login.as_view(),name="login"),
    path('user/',UserView.as_view(),name="user"),
    # path('addfiles',addfiles.as_view(),name="addfiles"),
    path('Verifyuser/<int:id>',Verifyuser.as_view(),name='verifyuser'),
    path('Rejectuser/<int:id>',Rejectuser.as_view(),name='rejectuser'),
    path('base',base.as_view(),name="base"),
    path('change',change.as_view(),name="change"),
    path('edit',edit.as_view(),name="edit"),
    path('profile',profile.as_view(),name="profile"),
    path('rating',rating.as_view(),name="rating"),
    path('register/',register.as_view(),name="register"),
    path('user_home',user_home.as_view(),name="user_home"),
    path('viewfiles',viewfiles.as_view(),name="viewfiles"),
    path('admin_home',admin_home.as_view(),name="admin_home"),
    path('blockedUser',blockedUser.as_view(),name="blockedUser"),
    path('edit/<int:file_id>/', EditFileView.as_view(), name='edit_file'),
    path('delete/<int:file_id>/', DeleteFileView.as_view(), name='delete_file'),
    # urls.py

    path('filelist', FileListView.as_view(), name='file_list'),
    path('addfiles/', UploadFileView.as_view(), name='upload_file'),
    path('download/<int:file_id>/', DownloadFileView.as_view(), name='download_file'),
    path('rate/', RatingView.as_view(), name='rating_form'),
]





