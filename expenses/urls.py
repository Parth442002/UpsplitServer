from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ExpenseList.as_view()),
    path('<uuid:expense_id>/', views.DetailUpdateExpenseView.as_view()),
]
