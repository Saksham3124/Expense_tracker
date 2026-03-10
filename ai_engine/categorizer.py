from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from expenses.models import Expense


def predict_category(description):

    # default base training data
    training_data = [
        ("uber ride", "Transport"),
        ("ola cab", "Transport"),
        ("rapido ride", "Transport"),
        ("bus ticket", "Transport"),
        ("metro ticket", "Transport"),

        ("pizza", "Food"),
        ("burger", "Food"),
        ("zomato order", "Food"),
        ("restaurant dinner", "Food"),

        ("movie ticket", "Entertainment"),
        ("cinema", "Entertainment"),
        ("netflix subscription", "Entertainment"),

        ("amazon shopping", "Shopping"),
        ("buy clothes", "Shopping"),
        ("flipkart order", "Shopping"),
    ]

    # add user expense history to training data
    expenses = Expense.objects.select_related("category").all()

    for expense in expenses:
        if expense.description and expense.category:
            training_data.append((expense.description.lower(), expense.category.name))


    texts = [item[0] for item in training_data]
    labels = [item[1] for item in training_data]


    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    prediction = model.predict(vectorizer.transform([description.lower()]))

    return prediction[0]