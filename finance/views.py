import datetime
from finance import models
from finance.models import Budget, Category, Expense, Income
from finance.serializers import ExpenseSerializer, IncomeSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate  # <-- Import the authenticate function
from rest_framework.authtoken.models import Token
from django.db.models import Sum

# Category View
class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        category_data = [{'id': category.id, 'name': category.name} for category in categories]
        return Response(category_data)

    def post(self, request):
        category_name = request.data.get('name')
        new_category = Category.objects.create(name=category_name)
        return Response({'id': new_category.id, 'name': new_category.name}, status=status.HTTP_201_CREATED)

# Income View
class IncomeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)

        # Optional Filters
        category_id = request.query_params.get('category_id')
        if category_id:
            incomes = incomes.filter(category_id=category_id)

        amount = request.query_params.get('amount')
        if amount:
            incomes = incomes.filter(amount=amount)

        date = request.query_params.get('date')
        if date:
            incomes = incomes.filter(date=date)

        income_data = IncomeSerializer(incomes, many=True)
        return Response(income_data.data)

    def post(self, request):
        amount = request.data.get('amount')
        category_id = request.data.get('category_id')
        category = Category.objects.get(id=category_id)  # Get the category by ID
        income = Income.objects.create(user=request.user, amount=amount, category=category)
        income_data = IncomeSerializer(income)  # Serialize the created object
        return Response(income_data.data, status=status.HTTP_201_CREATED)

# Expense View
class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        # Optional Filters
        category_id = request.query_params.get('category_id')
        if category_id:
            expenses = expenses.filter(category_id=category_id)

        amount = request.query_params.get('amount')
        if amount:
            expenses = expenses.filter(amount=amount)

        date = request.query_params.get('date')
        if date:
            expenses = expenses.filter(date=date)

        expense_data = ExpenseSerializer(expenses, many=True)
        return Response(expense_data.data)

    def post(self, request):
        amount = request.data.get('amount')
        category_id = request.data.get('category_id')
        category = Category.objects.get(id=category_id)  # Get the category by ID
        expense = Expense.objects.create(user=request.user, amount=amount, category=category)
        expense_data = ExpenseSerializer(expense)  # Serialize the created object
        return Response(expense_data.data, status=status.HTTP_201_CREATED)
    
# Budget View
class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budget = Budget.objects.get(user=request.user)
        return Response({'amount': budget.amount})

    def post(self, request):
        amount = request.data.get('amount')
        month = request.data.get('month')
        year = request.data.get('year')

        if not all([amount, month, year]):
            return Response({'error': 'Amount, month, and year are required'}, status=400)

        budget, created = Budget.objects.update_or_create(
            user=request.user,
            month=month,
            year=year,
            defaults={'amount': amount}
        )

        return Response({
            'message': 'Budget set successfully',
            'budget_amount': budget.amount,
            'month': budget.month,
            'year': budget.year
        })
# Budget Summary View
class BudgetSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the current date and time to default month and year
        now = datetime.datetime.now()
        month = int(request.query_params.get('month', now.month))  # Ensure month is an integer
        year = int(request.query_params.get('year', now.year))  # Ensure year is an integer

        try:
            # Fetch the user's budget for the given month and year
            budget = Budget.objects.get(user=request.user, month=month, year=year)
        except Budget.DoesNotExist:
            return Response({
                'error': 'No budget set for this user in this month/year.'
            }, status=404)

        # Calculate total income for the specified month and year
        total_income = Income.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total_income=Sum('amount'))['total_income'] or 0

        # Calculate total expense for the specified month and year
        total_expense = Expense.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

        # Calculate balance and budget difference
        balance = total_income - total_expense
        budget_difference = budget.amount - total_expense

        # Return the response with calculated values
        return Response({
            'budget_amount': budget.amount,
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'budget_difference': budget_difference
        })

# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to log in

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # If user is authenticated, generate the auth token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Transaction View
class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)

        # Create a common structure
        transactions = []

        for income in incomes:
            transactions.append({
                'id': income.id,
                'type': 'income',
                'amount': income.amount,
                'category': income.category.name,
                'date': income.date
            })

        for expense in expenses:
            transactions.append({
                'id': expense.id,
                'type': 'expense',
                'amount': expense.amount,
                'category': expense.category.name,
                'date': expense.date
            })

        # Sort by date (optional, if you want newest first)
        transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)

        return Response(transactions)

