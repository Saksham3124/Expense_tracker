from django import forms
from .models import Category, Expense


from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ["amount","description","category","date","payment_method"]

        widgets = {
"amount": forms.NumberInput(attrs={"class":"w-full border rounded-lg px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"}),
"description": forms.TextInput(attrs={"class":"w-full border rounded-lg px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"}),
"category": forms.Select(attrs={"class":"w-full border rounded-lg px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"}),
"date": forms.DateInput(attrs={"type":"date","class":"w-full border rounded-lg px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"}),
"payment_method": forms.Select(attrs={"class":"w-full border rounded-lg px-3 py-2 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100"}),
}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

# forms.py

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "budget"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class":"w-full border rounded-lg p-2"
            }),

            "budget": forms.NumberInput(attrs={
                "class":"w-full border rounded-lg p-2",
                "placeholder":"Optional budget amount"
            })
        }