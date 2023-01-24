from rest_framework import status
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


class ExpenseList(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]


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
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
