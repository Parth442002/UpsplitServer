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
        fields = ('id', 'lender', 'borrowers', 'amount_borrowed', 'amount_repayed',
                  'timestamp', 'title', 'category')

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
        instance.amount_borrowed = validated_data.get(
            'amount_borrowed', instance.amount_borrowed)
        instance.amount_repayed = validated_data.get(
            'amount_repayed', instance.amount_repayed)
        instance.timestamp = validated_data.get(
            'timestamp', instance.timestamp)
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)

        # update or create borrowers
        instance.borrowers.all().delete()
        for borrower_data in borrowers_data:
            instance.borrowers.create(**borrower_data)
        instance.save()

        return instance
