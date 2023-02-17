from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ExpenseList.as_view()),
    path('user_id=<uuid:user_id>/', views.UserExpenseList.as_view()),
    path('<uuid:expense_id>/', views.DetailUpdateExpenseView.as_view()),

    # Url to repay expense
    path("<uuid:expense_id>/<uuid:borrower_id>/repay/",
         views.RepayExpenseView.as_view()),
]
