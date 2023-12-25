from django.urls import path
from .views import *

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit_data'),
    path('getData/<int:id>/', GetMountainPassView.as_view(), name='get_mountain_pass'),
    path('editData/<int:id>/', EditMountainPassView.as_view(), name='edit_mountain_pass'),
    path('userMountainPassList/', GetUserMountainPassListView.as_view(), name='get_user_mountain_pass_list'),
    # ...
]
