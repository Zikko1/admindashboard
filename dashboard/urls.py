from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/',views.index, name='dashboard-index'),
    path('members/',views.members, name='dashboard-members'),
    path('members/detail/<int:pk>/',views.admins_details, name='dashboard-admins-details'),
    path('contributions/',views.contributions, name='dashboard-contributions'),
    path('contributions/delete/<int:pk>/',views.contributions_delete, name='dashboard-contributions-delete'),
    path('contributions/update/<int:pk>/',views.contributions_update, name='dashboard-contributions-update'),
    path('Loans/',views.Loans, name='dashboard-loans'),
    path('Loans/approved/<int:pk>/',views.approved_loans,name='dashboard-approved'),
    path('Loans/pending/<int:pk>/',views.pending_loans,name='dashboard-pending'),
]
