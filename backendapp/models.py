from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum, F
from decimal import Decimal


class Category(models.Model):
    TYPE_CHOISES = (
        ('expense', 'Dépense'),
        ('income', 'Révenu')
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOISES)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=30)
    status = models.SmallIntegerField(default=0, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='category_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='category_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.name} - ({self.type})"
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=18, decimal_places=3, default=0.00, null=True)
    account = models.ForeignKey('Account', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='account_transactions')
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.now)
    photo = models.FileField(upload_to="transactions_photos/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transactions')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category_transactions')
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transaction_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transaction_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} (Mt. {self.amount})"
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    

class Budget(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=18, decimal_places=3, default=0.00, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_budget')
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='budget_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='budget_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.title} - (Initial: {self.total_amount})"
        
    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        unique_together = ('user', 'category')
    
    
class Account(models.Model):
    TYPE_CHOICES = (
        ('orange_money', 'Orange Money'),
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Banque'),
        ('others', 'Autres')
    )
    
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    balance = models.DecimalField(max_digits=18, decimal_places=3)
    description = models.TextField(null=True, blank=True)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='currency_accounts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_accounts')
    status = models.SmallIntegerField(default=1, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.name} - (Mt. Actuel: {self.current_balance()})"
    
    def current_balance(self):
        transactions = Transaction.objects.filter(account=self)
        total_debit_income = transactions.filter(category__type='income', amount__lt=0).aggregate(total=Sum(F('amount')))['total'] or Decimal('0.00')
        total_debit_expense = transactions.filter(category__type='expense', amount__lt=0).aggregate(total=Sum(F('amount')))['total'] or Decimal('0.00')
        total_credit = transactions.filter(amount__gt=0).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        return self.balance + total_credit + total_debit_income + total_debit_expense
    
    def deduce_balance(self, amount):
        self.balance -= Decimal(amount)
        self.save()
        
        return str(self.balance)
    
    def increase_balance(self, amount):
        self.balance += Decimal(amount)
        self.save()
        
        return str(self.balance)
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    
class Transfer(models.Model):#fait le
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_account')
    recipient_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient_account')
    amount = models.DecimalField(max_digits=18, decimal_places=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transfer')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfer_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfer_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.sender_account.account_number} vers {self.recipient_account.account_number}"
    
    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'
    

class Currency(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    status = models.SmallIntegerField(default=1, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='currency_created')
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='currency_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} - ({self.code})"
    
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
      
