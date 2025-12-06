from src.core import load_reviews_from_csv, analyze_reviews

# загрузка данных
reviews = load_reviews_from_csv("data/sample_reviews.csv")
print(f"Было загружено {len(reviews)} отзывов")

# анализ
analyzed = analyze_reviews(reviews)

# выводим примеры
for i, r in enumerate(analyzed[:3]):
    print(f"\n{r['review_text']}")
    print(f"Полярность: {r['polarity']:.2f}, Метка: {r['sentiment_label']}")
