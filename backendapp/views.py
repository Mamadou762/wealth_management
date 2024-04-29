import pdb
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.middleware.csrf import get_token

from backendapp.models import *
from backendapp.forms import *


def index(request):
    return render(request, 'backendapp/pages/dashboard.html')


## Transaction ##
class TransactionListView(ListView):
    model = Transaction
    template_name = 'backendapp/pages/transaction/transactions.html'
    paginate_by = 5
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transfer_form'] = TransferForm()
        return context
    
    
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'backendapp/pages/transaction/transactions.html'
    success_url = reverse_lazy('transactions')
    form_class = TransactionForm

    def form_valid(self, form):
        category = form.save(commit=False)
        category.created_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class TransactionUpdateView(UpdateView):
    model = Transaction
    template_name = 'backendapp/pages/transaction/transactions.html'
    success_url = reverse_lazy('transactions')
    form_class = TransactionForm
    
    
class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('transactions')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        return redirect(self.success_url)


## Account ##
class AccountListView(ListView):
    model = Account
    template_name = 'backendapp/pages/account/accounts.html'
    paginate_by = 5
    
    
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = 'backendapp/pages/account/create-account.html'
    success_url = reverse_lazy('accounts')
    form_class = AccountForm

    def form_valid(self, form):
        account = form.save(commit=False)
        account.user = self.request.user
        account.created_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class AccountUpdateView(UpdateView):
    model = Account
    template_name = 'backendapp/pages/account/update-account.html'
    success_url = reverse_lazy('accounts')
    form_class = AccountForm
    
    def form_valid(self, form):
        budget = form.save(commit=False)
        budget.user = self.request.user
        budget.updated_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('accounts')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        return redirect(self.success_url)
    

def update_account_status(request, pk):
    account = Account.objects.get(pk=pk)
    
    if account.status == 1:
        account.status = 0
    else:
        account.status = 1
        
    account.save()
    
    messages.success(request, 'Compte modifiée avec succès.')
    return redirect('accounts')


## Budget ##
class BudgetListView(ListView):
    model = Budget
    template_name = 'backendapp/pages/budget/budgets.html'
    paginate_by = 5
    
    
class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'backendapp/pages/budget/create-budget.html'
    success_url = reverse_lazy('budgets')
    form_class = BudgetForm

    def form_valid(self, form):
        budget = form.save(commit=False)
        budget.user = self.request.user
        budget.status = 1
        budget.created_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class BudgetUpdateView(UpdateView):
    model = Budget
    template_name = 'backendapp/pages/budget/update-budget.html'
    success_url = reverse_lazy('budgets')
    form_class = BudgetForm
    
    def form_valid(self, form):
        budget = form.save(commit=False)
        budget.user = self.request.user
        budget.updated_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class BudgetDeleteView(DeleteView):
    model = Budget
    success_url = reverse_lazy('budgets')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        return redirect(self.success_url)
    

def update_budget_status(request, pk):
    budget = Budget.objects.get(pk=pk)
    
    if budget.status == 1:
        budget.status = 0
    else:
        budget.status = 1
        
    budget.save()
    
    messages.success(request, 'Budget modifiée avec succès.')
    return redirect('budgets')
    

## Category ##
class CategoryListView(ListView):
    model = Category
    template_name = 'backendapp/pages/category/categories.html'
    paginate_by = 2
    
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'backendapp/pages/category/create-category.html'
    success_url = reverse_lazy('categories')
    form_class = CategoryForm
    initial = {
        'type': 'income'
    }
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.created_by = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'backendapp/pages/category/update-category.html'
    success_url = reverse_lazy('categories')
    form_class = CategoryForm
    initial = {
        'type': 'income'
    }
    

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        messages.success(request, 'Categorie supprimée avec succès.')
        return redirect(self.success_url)
    
    
def update_category_status(request, pk):
    category = Category.objects.get(pk=pk)
    
    if category.status == 1:
        category.status = 0
    else:
        category.status = 1
        
    category.save()
    
    messages.success(request, 'Categorie modifiée avec succès.')
    return redirect('categories')
    

## Currency ##
class CurrencyView(View):
    template_name = 'backendapp/pages/currency/currencies.html'
    
    def get(self, request):
        currency_id = request.GET.get('currencyId')
        
        if currency_id:
            currency = Currency.objects.get(pk=currency_id)
            
            data = {
                'id': currency.id,
                'name': currency.name,
                'code': currency.code
            }
            
            return JsonResponse(data, safe=False)
            
        currencies = Currency.objects.all()
        paginator = Paginator(currencies, 2)
        
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        form = CurrencyForm()
        context = {
            'form': form,
            "page_obj": page_obj
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = CurrencyForm(request.POST)
        
        if form.is_valid():
            currency = form.save(commit=False)
            currency.created_by = request.user
            currency.save()
            
            messages.success(request, 'Dévise ajouté avec succès.')
            return self.get(request)
        else:
            messages.error(request, f'{form.errors}')
            context = {
                'form': form
            }
            
            return self.get(request)
        
    def patch(self, request, *args, **kwargs):
        currency_id = request.GET.get('currency_id')
        name = request.GET.get('name')
        code = request.GET.get('code')

        if currency_id:
            currency = Currency.objects.get(id=currency_id)
            currency.name = name
            currency.code = code
            currency.save()
            
            messages.success(request, 'Devise modifié avec succès.')
        else:
            messages.error(request, 'Erreur lors de la suppression de la devise.')
        return self.get(request)
        
    def delete(self, request):
        currency_id = request.GET.get('currency_id')

        if currency_id:
            currency = Currency.objects.get(id=currency_id)
            currency.delete()
            messages.success(request, 'Devise supprimée avec succès.')
        else:
            messages.error(request, 'Erreur lors de la suppression de la devise.')
        return self.get(request)


## Transfers ##
class TransferListView(ListView):
    model = Transfer
    template_name = 'backendapp/pages/transfer/transfers.html'
    paginate_by = 5
    
    
class TransferCreateView(LoginRequiredMixin, CreateView):
    model = Transfer
    template_name = 'backendapp/pages/transfer/transfers.html'
    success_url = reverse_lazy('transfers')
    form_class = TransferForm

    def form_valid(self, form):
        sender_account = form.cleaned_data['sender_account']
        recipient_account = form.cleaned_data['recipient_account']
        amount = form.cleaned_data['amount']
        
        m1 = sender_account.deduce_balance(amount)
        m2 = recipient_account.increase_balance(amount)
        
        transfer = form.save(commit=False)
        transfer.user = self.request.user
        transfer.created_by = self.request.user
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Veuillez corriger les erreurs ci-dessous. {form.errors}")
        return super().form_invalid(form)
    
    
class TransferUpdateView(UpdateView):
    model = Transfer
    template_name = 'backendapp/pages/transfer/transfers.html'
    success_url = reverse_lazy('transfers')
    form_class = TransferForm
    
    
class TransferDeleteView(DeleteView):
    model = Transfer
    success_url = reverse_lazy('transfer')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        
        return redirect(self.success_url)


def user(request):
    return render(request, 'backendapp/pages/user/users.html')


def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse(data={'csrf_token': token})