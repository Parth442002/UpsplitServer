from rest_framework import serializers
from .models import Borrower, Expense
import io
from rest_framework.parsers import JSONParser

from django.contrib.auth import get_user_model
user_model = get_user_model()


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ('id', 'user', 'amount_borrowed', 'amount_repayed',)


class ExpenseSerializer(serializers.ModelSerializer):
    borrowers = BorrowerSerializer(many=True)

    class Meta:
        model = Expense
        fields = ('id',
                  'timestamp', 'title', 'desc', 'lender', 'borrowers', 'totalexpense', 'lenders_share', "totalborrowed", "totalrepayed", "is_settled"
                  )

    def create(self, validated_data):
        borrowers_data = validated_data.pop('borrowers')
        expense = Expense.objects.create(**validated_data)
        for borrower in borrowers_data:
            expense.borrowers.create(**borrower)
            print("This does work indeed")
        expense.save()
        print("this function was called successfully")
        return expense

    def update(self, instance, validated_data):
        borrowers_data = validated_data.pop('borrowers')

        instance.lender = validated_data.get('lender', instance.lender)

        instance.lenders_share = validated_data.get(
            'lenders_share', instance.lenders_share)
        instance.totalexpense = validated_data.get(
            'totalexpense', instance.totalexpense)
        instance.totalborrowed = validated_data.get(
            'totalborrowed', instance.totalborrowed)
        instance.totalrepayed = validated_data.get(
            'total_borrowed', instance.totalrepayed)
        instance.is_settled = validated_data.get(
            'is_settled', instance.is_settled)

        # update or create borrowers
        instance.borrowers.all().delete()
        for borrower_data in borrowers_data:
            instance.borrowers.create(**borrower_data)
        instance.save()

        return instance
