from django.urls import path
from .views import *

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit_data'), # Передача данных для создания новой записи перевала
    path('createUser/', AddNewUser.as_view(), name='create_user'),
    path('getData/<int:pk>/', GetMountainPassView.as_view(), name='get_mountain_pass'),
    path('editData/<int:pk>/', EditMountainPassView.as_view(), name='edit_mountain_pass'),
    path('userMountainPassList/', GetUserMountainPassListView.as_view(), name='get_user_mountain_pass_list'),
    # ...
]
