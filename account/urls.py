from django.urls import path
from account import views

urlpatterns = [
    path('account/register/', views.register_user, name="sign_up"),
    path('account/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('account/', views.user_details, name="my_account"),
    path('account/change-password/', views.update_password, name="update_password"),
    path('account/forgot-password/', views.send_reset_password_email, name="forgot_password"),
    path('account/reset-password/', views.reset_password, name="reset_password"),
    path('account/delete-user/', views.delete_user, name='delete_user'),
]
