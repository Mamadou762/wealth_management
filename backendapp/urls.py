from django.urls import path
from backendapp.views import *


urlpatterns = [
    path('', index, name='dashboard'),

    ## Transaction ##
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('transactions/update/<int:pk>/', TransactionUpdateView.as_view(), name='transaction-update'),
        
    ## Transfer ##
    path('transfers/', TransferListView.as_view(), name='transfers'),
    path('transfers/create/', TransferCreateView.as_view(), name='transfer-create'),
    path('transfers/delete/<int:pk>/', TransferDeleteView.as_view(), name='transfer-delete'),
    path('transfers/update/<int:pk>/', TransferUpdateView.as_view(), name='transfer-update'),
    
    ## Account ##
    path('accounts/', AccountListView.as_view(), name='accounts'),
    path('accounts/create/', AccountCreateView.as_view(), name='account-create'),
    path('accounts/delete/<int:pk>/', AccountDeleteView.as_view(), name='account-delete'),
    path('accounts/update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
    path('account/update-status/<int:pk>/', update_account_status, name='update-account-status'),
    
    ## Budget ##
    path('budgets/', BudgetListView.as_view(), name='budgets'),
    path('budgets/create/', BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/delete/<int:pk>/', BudgetDeleteView.as_view(), name='budget-delete'),
    path('budgets/update/<int:pk>/', BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/update-status/<int:pk>/', update_budget_status, name='update-budget-status'),

    ## Category ##
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/update-status/<int:pk>/', update_category_status, name='update-category-status'),
    
    ## Currency ##
    path('currencies/', CurrencyView.as_view(), name='currencies'),
    
    ## User ##
    path('users/', user, name='users'),
    
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token')
]
