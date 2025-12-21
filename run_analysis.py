# Нет докстрингов и аннотации типов

from src.core import (
    load_reviews_from_csv,
    analyze_reviews,
    compute_statistics,
    export_results,
    plot_sentiment_distribution
)
# Правильный импорт (если бы у вас был модуль, для примера назову его `my_module`, и `run_analysis.py` находился бы под `src`):
# from .my_module import (
#     load_reviews_from_csv,
#     analyze_reviews,
#     compute_statistics,
#     export_results,
#     plot_sentiment_distribution
# )


def main():
    # загрузка
    print("Загрузка отзывов...")
    reviews = load_reviews_from_csv("data/imdb_reviews.csv")  # Не стоит фиксировать в коде название файла. Это должен задавать юзер

    # анализ
    print("Анализ тональности...")
    analyzed = analyze_reviews(reviews)

    # вывод статистики
    stats = compute_statistics(analyzed)
    total = sum(stats.values())

    print("\n📊 Статистика тональности:")
    print("-" * 30)
    for label, count in stats.items():
        percent = count / total * 100 if total > 0 else 0
        print(f"{label.capitalize()}: {count} ({percent:.1f}%)")

    # экспорт и визуализация
    export_results(analyzed, "output")
    plot_sentiment_distribution(analyzed, "output/plots")


if __name__ == "__main__":
    main()
