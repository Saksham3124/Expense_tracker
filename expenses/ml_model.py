from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from expenses.models import Expense

vectorizer = None
model = None


def train_model():

    global vectorizer, model

    expenses = Expense.objects.select_related("category").all()

    texts = []
    labels = []

    for e in expenses:
        if e.description and e.category:
            texts.append(e.description.lower())
            labels.append(e.category.name)

    if len(texts) < 5:
        return False

    vectorizer = TfidfVectorizer(stop_words="english")

    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()

    model.fit(X, labels)

    return True


def predict_category(text):

    global vectorizer, model

    if model is None or vectorizer is None:
        if not train_model():
            return None

    X = vectorizer.transform([text.lower()])

    prediction = model.predict(X)[0]

    return prediction