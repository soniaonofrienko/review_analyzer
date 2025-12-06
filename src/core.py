
from typing import List, Dict, Tuple
import pandas as pd

# каждый отзыв
Review = Dict[str, str]  # пример: {"text": "great!", "category": "movie"}

# результат анализа
AnalyzedReview = Dict[str, object]  # {"text": "...", "polarity": 0.8, "label": "positive"}


def load_reviews_from_csv(path: str) -> List[Review]:  # считывает отзывы
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Не удалось найти файл: {path}")

    if 'review_text' not in df.columns:
        raise ValueError("Не удалось найти колонку 'review_text'")

    # заменяем пропущенные знвчения на пустые строки и приводим все объекты к строкам
    df = df.fillna("")
    df = df.astype(str)

    # преобразуем в список словарей
    return df.to_dict(orient='records')


def predict_sentiment(text: str) -> Tuple[float, str]:  # анализирует тональность одного отзыва
    pass


def analyze_reviews(reviews: List[Review]) -> List[AnalyzedReview]:  # применяет ко всем отзывам
    pass


def compute_statistics(analyzed: List[AnalyzedReview]) -> Dict[str, int]:  # считает статистику
    pass


def export_results(analyzed: List[AnalyzedReview], output_dir: str) -> None:  # сохраняет результаты
    pass
