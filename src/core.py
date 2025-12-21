# Импорты не отсортированы, нет докстрингов и аннотации типов

from typing import List, Dict, Tuple  # Такой способ аннотации типа устарел. Вместо него используйте 'list[...]' / `dict[..., ...]` / `tuple[...]`
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os

_analyzer = SentimentIntensityAnalyzer()

# каждый отзыв
Review = Dict[str, str]  # пример: {"text": "great!", "category": "movie"}

# результат анализа
AnalyzedReview = Dict[str, object]  # {"text": "...", "polarity": 0.8, "label": "positive"}


def load_reviews_from_csv(path: str) -> List[Review]:
    """Загружает отзывы из CSV-файла.

    Ожидает наличие колонки 'review_text'.
    Возвращает список словарей — по одному на строку.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось найти файл: {path}")

    if 'review_text' not in df.columns:
        raise ValueError("Не удалось найти колонку 'review_text'")

    # заменяем пропущенные значения на пустые строки и приводим все объекты к строкам
    df = df.fillna("")
    df = df.astype(str)

    # преобразуем в список словарей
    return df.to_dict(orient='records')


def predict_sentiment(text: str) -> Tuple[float, str]:
    """Анализирует тональность одного текста с помощью VADER.

    Возвращает кортеж (polarity: float от -1 до 1, метка: str).
    Метка — одна из: 'positive', 'negative', 'neutral'.
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0, "neutral"

    scores = _analyzer.polarity_scores(text)
    compound = scores['compound']  # агрегированный скор от -1 до +1

    if compound >= 0.2:
        label = "positive"
    elif compound <= -0.25:
        label = "negative"
    else:
        label = "neutral"

    return compound, label


def analyze_reviews(reviews: List[Review]) -> List[AnalyzedReview]:
    """Применяет анализ тональности ко всем отзывам.

    Возвращает новый список, где к каждому отзыву добавлены
    поля 'polarity' и 'sentiment_label'.
    """
    analyzed = []
    for review in reviews:
        # сохраняем исходный отзыв
        new_review = review.copy()
        # анализируем текст
        text = review.get("review_text", "")
        polarity, label = predict_sentiment(text)
        # добавляем результаты
        new_review["polarity"] = polarity  # Expected type 'str' (matched generic type '_VT'), got 'float' instead
        new_review["sentiment_label"] = label
        analyzed.append(new_review)
    return analyzed


def compute_statistics(analyzed: List[AnalyzedReview]) -> Dict[str, int]:
    """Считает количество отзывов по меткам тональности.

    Возвращает словарь вида {'positive': 10, 'negative': 5, 'neutral': 2}.
    """
    statistics = {"positive": 0, "negative": 0, "neutral": 0}
    for review in analyzed:
        label = review.get("sentiment_label")
        if label in statistics:
            statistics[label] += 1
    return statistics


def export_results(analyzed: List[AnalyzedReview], output_dir: str) -> None:
    """Сохраняет результаты анализа в файлы.

    Создаёт:
    - reviews_with_sentiment.csv
    - sentiment_report.txt
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. csv с результатами
    df = pd.DataFrame(analyzed)
    df.to_csv(os.path.join(output_dir, "reviews_with_sentiment.csv"), index=False)

    # 2. текстовый отчёт
    stats = compute_statistics(analyzed)
    report_path = os.path.join(output_dir, "sentiment_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Анализ тональности отзывов\n")
        f.write("=" * 30 + "\n")
        f.write(f"Всего отзывов: {sum(stats.values())}\n")
        f.write(f"Позитивных: {stats['positive']}\n")
        f.write(f"Негативных: {stats['negative']}\n")
        f.write(f"Нейтральных: {stats['neutral']}\n")

    print(f"Результаты были сохранены в папке {output_dir}")


def plot_sentiment_distribution(analyzed: List[Dict[str, object]], output_dir: str) -> None:
    """Создаёт и сохраняет круговую диаграмму распределения тональности.

    Диаграмма сохраняется как 'sentiment_pie.png' в указанной папке.
    """
    stats = compute_statistics(analyzed)
    labels = list(stats.keys())
    sizes = list(stats.values())
    colors = ['#4CAF50', '#F44336', '#9E9E9E']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Распределение тональности отзывов")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "sentiment_pie.png"))
    plt.close()
    print(f"Диаграмма была сохранена: {os.path.join(output_dir, 'sentiment_pie.png')}")

