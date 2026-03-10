from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('add-expense/', views.add_expense, name="add_expense"),
    path('expenses/', views.expense_list, name='expense_list'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path("export-excel/", views.export_expenses_excel, name="export_excel"),
    path("predict-category/", views.predict_category_api, name="predict_category_api"),
    path("category/<int:id>/budget/", views.update_budget, name="update_budget"),

]
