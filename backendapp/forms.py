from django import forms
from backendapp.models import *


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer un nom de categorie'}),
            'type': forms.Select(attrs={'class': 'form-select'}, choices=Category.TYPE_CHOISES),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Laisser une description...', 'style': 'height: 100px'}),
            'icon': forms.TextInput(attrs={'type': 'hidden'})
        }
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        
        
class CurrencyForm(forms.ModelForm):
    
    class Meta:
        model = Currency
        exclude = ['status', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer un nom'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer le code'})
        }
        

class BudgetForm(forms.ModelForm):
    
    class Meta:
        model = Budget
        exclude = ['user', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Veuillez entrer une désignation'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Laisser une description...', 'style': 'height: 100px'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=[(category.id, category.name) for category in Category.objects.filter(type='expense', status=1)])
        }
    
    
class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        exclude = ['user', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Laisser une description...', 'style': 'height: 100px'}),
            'category': forms.Select({'class': 'form-select'}, choices=[]),
            'account': forms.Select({'class': 'form-select'}, choices=[]),
            'date': forms.DateTimeInput(attrs={'class': 'form-control input-with-bottom-line', 'id': 'dateEnd', 'type': 'date'}),
            'photo': forms.ClearableFileInput(
                attrs={'class': 'form-control input-with-bottom-line', 'type': 'file'})
        }
                
    def get_categories(self):
        return Category.objects.filter(status=1)
    
    
class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        exclude = ['status', 'user', 'created_by', 'updated_by', 'created_at', 'updated_at']
                
        widgets = {
            'name': forms.TextInput({'class': 'form-control', 'placeholder': 'Veuillez rentrez le nom (désignation)'}),
            'type': forms.Select(attrs={'class': 'form-select'}, choices=Account.TYPE_CHOICES),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Laisser une description...', 'style': 'height: 100px'}),
            'currency': forms.Select(attrs={'class': 'form-select'}, choices=[(currency.id, currency.name) for currency in Currency.objects.filter(status=1)]),
        }
        
        
class TransferForm(forms.ModelForm):
    
    class Meta:
        model = Transfer
        exclude = ['user', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
        widgets = {
            'sender_account': forms.Select(attrs={'class': 'form-select'}, choices=[]),
            'recipient_account': forms.Select(attrs={'class': 'form-select'}, choices=[]),
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }