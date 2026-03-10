from datetime import datetime
from urllib import request
from django.core import paginator
from django.shortcuts import redirect, render
import expenses
from .models import Expense
from expenses.forms import ExpenseForm
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from expenses.models import Category
from django.core.paginator import Paginator
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import numbers
from .models import Category
from django.http import JsonResponse
from collections import defaultdict
from django.utils import timezone
from .ml_model import predict_category
from .ml_model import train_model

@login_required
def add_expense(request):

    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)

        if form.is_valid():

            expense = form.save(commit=False)

            description = form.cleaned_data["description"]

            predicted = predict_category(description)

            # Find predicted category for this user
            category = None
            if predicted:
                category = Category.objects.filter(
                    name__iexact=predicted,
                    user=request.user
                ).first()

            # Only apply AI category if user didn't manually select one
            if not expense.category and category:
                expense.category = category

            expense.user = request.user
            expense.save()

            # retrain ML model with new expense
            train_model()

            return redirect("dashboard")

    else:
        form = ExpenseForm(user=request.user)

    return render(request, "add_expense.html", {"form": form})
@login_required
def expense_list(request):

    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')

    categories = Category.objects.filter(user=request.user)

    category_id = request.GET.get("category")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search_query = request.GET.get("search")

    if search_query:
        expenses = expenses.filter(description__icontains=search_query)

    if category_id:
        expenses = expenses.filter(category_id=category_id)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Budget Alerts

    alerts = []

    for category in categories:

        total = Expense.objects.filter(
            user=request.user,
            category=category
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        if category.budget and total > category.budget:
            alerts.append({
                "name": category.name,
                "spent": total,
                "budget": category.budget
            })
    context = {
        "expenses": page_obj,
        "categories": categories,
        "selected_category": category_id,
        "start_date": start_date,
        "end_date": end_date,
        "search_query": search_query,
        "page_obj": page_obj,
        "alerts": alerts
    }

    return render(request, "expense_list.html", context)

@login_required
def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect("expense_list")

    else:
        form = ExpenseForm(instance=expense)

    return render(request, "edit_expense.html", {"form": form})

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect("expense_list")
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    transaction_count = expenses.count()

    current_month = datetime.now().month
    monthly_expense = expenses.filter(date__month=current_month).aggregate(Sum('amount'))['amount__sum'] or 0

    recent_expenses = expenses.order_by('-created_at')[:5]

    category_data = expenses.values('category__name').annotate(total=Sum('amount'))
    category_labels = []
    category_amounts = []
    for item in category_data:
        category_labels.append(item['category__name'])
        category_amounts.append(float(item['total']))

    monthly_data = expenses.annotate(month=TruncMonth('date')) \
                    .values('month') \
                    .annotate(total=Sum('amount')) \
                    .order_by('month')

    month_labels = []
    month_amounts = []

    for item in monthly_data:
        month_labels.append(item['month'].strftime("%B"))
        month_amounts.append(float(item['total']))

    # ----- AI INSIGHTS -----

    insights = []

    # highest spending category
    if category_data:
        highest = max(category_data, key=lambda x: x["total"])
        insights.append(
            f"Your highest spending category is {highest['category__name'] } with ₹{highest['total']}."
        )

    # percentage spending
    if total_expense > 0:
        for item in category_data:
            percent = round((item["total"] / total_expense) * 100, 1)

            if percent > 40:
                insights.append(
                    f"You spent {percent}% of your expenses on {item['category__name']}."
                )

    # monthly comparison
    current_month = timezone.now().month
    last_month = current_month - 1

    current_total = expenses.filter(date__month=current_month).aggregate(Sum("amount"))["amount__sum"] or 0
    last_total = expenses.filter(date__month=last_month).aggregate(Sum("amount"))["amount__sum"] or 0

    if last_total > 0:

        if current_total > last_total:
            change = round(((current_total - last_total) / last_total) * 100, 1)
            insights.append(
                f"Your spending increased by {change}% compared to last month."
            )

        elif current_total < last_total:
            change = round(((last_total - current_total) / last_total) * 100, 1)
            insights.append(
                f"Your spending decreased by {change}% compared to last month."
            )
    
    budget_alerts = []

    current_month = timezone.now().month

    monthly_categories = expenses.filter(date__month=current_month) \
    .values("category__id", "category__name") \
    .annotate(total=Sum("amount"))
    for item in monthly_categories:

        category_id = item["category__id"]
        category_name = item["category__name"]
        total = item["total"]

        category = Category.objects.get(id=category_id)

        if category.budget and total > category.budget:

            budget_alerts.append(f"{category_name} spending exceeded ₹{category.budget} this month."
        )
    # ----- SMART ANALYTICS -----

    avg_spending = 0
    highest_day = None

    if expenses.exists():

        avg_spending = round(total_expense / transaction_count, 2)

        daily_spending = expenses.values("date") \
            .annotate(total=Sum("amount")) \
            .order_by("-total")

        if daily_spending:
            highest_day = daily_spending[0]

    # ----- EXPENSE PREDICTION -----

    predicted_next_month = 0

    monthly_totals = expenses.annotate(month=TruncMonth("date")) \
        .values("month") \
        .annotate(total=Sum("amount")) \
        .order_by("month")

    if len(monthly_totals) >= 2:

        last_month_total = monthly_totals[len(monthly_totals)-1]["total"]
        prev_month_total = monthly_totals[len(monthly_totals)-2]["total"]

        growth = last_month_total - prev_month_total

        predicted_next_month = last_month_total + growth
    context = {
    "total_expense": total_expense,
    "transaction_count": transaction_count,
    "monthly_expense": monthly_expense,
    "recent_expenses": recent_expenses,
    "category_labels": category_labels,
    "category_amounts": category_amounts,
    "month_labels": month_labels,
    "month_amounts": month_amounts,
    "insights": insights,
    "budget_alerts": budget_alerts,
    "avg_spending": avg_spending,
    "highest_day": highest_day,
    "predicted_next_month": predicted_next_month,
    }
    return render(request, "dashboard.html", context)

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "category_list.html", {"categories": categories})

@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST.get("name")
        budget = request.POST.get("budget")

        if name:
            Category.objects.create(
                name=name,
                budget=budget if budget else None,
                user=request.user
            )

            return redirect("category_list")

    return render(request, "add_category.html")


@login_required
def edit_category(request, id):

    category = get_object_or_404(Category, id=id, user=request.user)

    if request.method == "POST":

        name = request.POST.get("name")
        budget = request.POST.get("budget")

        category.name = name
        category.budget = budget if budget else None
        category.save()

        return redirect("category_list")

    return render(request, "edit_category.html", {"category": category})


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, user=request.user)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    return render(request, "delete_category.html", {"category": category})

@login_required
def export_expenses_excel(request):

    # Always initialize expenses first
    expenses = Expense.objects.filter(user=request.user)

    category_id = request.GET.get("category")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search_query = request.GET.get("search")

    if category_id and category_id != "None":
        expenses = expenses.filter(category_id=int(category_id))

    if start_date and start_date != "None":
        expenses = expenses.filter(date__gte=start_date)

    if end_date and end_date != "None":
        expenses = expenses.filter(date__lte=end_date)

    if search_query and search_query != "None":
        expenses = expenses.filter(description__icontains=search_query)


    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"

    headers = ["Date", "Description", "Category", "Amount", "Payment Method"]
    sheet.append(headers)

    for expense in expenses:
        sheet.append([
            expense.date.strftime("%Y-%m-%d"),
            expense.description,
            expense.category.name,
            float(expense.amount),
            expense.payment_method
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'

    workbook.save(response)

    return response


def predict_category_api(request):

    text = request.GET.get("text", "").strip()

    if not text:
        return JsonResponse({"category": None})

    category = predict_category(text)

    return JsonResponse({"category": category})


@login_required

def update_budget(request, id):

    category = get_object_or_404(Category, id=id, user=request.user)

    if request.method == "POST":
        budget = request.POST.get("budget")

        if budget:
            category.budget = budget
            category.save()

    return redirect("category_list")



