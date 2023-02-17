from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.http import Http404
from .models import Expense, Borrower
from .serializers import ExpenseSerializer, BorrowerSerializer


def get_object_or_404(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise Http404()


class ExpenseList(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]


class UserExpenseList(APIView):
    def get(self, request, user_id):
        expenses = Expense.objects.filter(Q(
            borrowers__user__id=user_id
        ) | Q(lender__id=user_id))
        serializer = ExpenseSerializer(expenses, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUpdateExpenseView(APIView):

    def get(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        serializer = ExpenseSerializer(expense)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            expense = serializer.save()
            return Response(ExpenseSerializer(expense).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        for borrower in expense.borrowers.all():
            # Deleting all the related borrowers
            Borrower.objects.filter(id=borrower.id).delete()
        # deleting the expense itself.
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RepayExpenseView(APIView):

    def post(self, request, expense_id, borrower_id):
        expense = get_object_or_404(Expense, id=expense_id)
        borrower = expense.borrowers.get(id=borrower_id)
        data = request.POST.get("amount_repayed")
        print(data, "workig")
        return Response(status=status.HTTP_202_ACCEPTED)
