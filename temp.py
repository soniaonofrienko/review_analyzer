from src.core import (
    load_reviews_from_csv,
    analyze_reviews,
    compute_statistics,
    export_results
)

reviews = load_reviews_from_csv("data/sample_reviews.csv")
analyzed = analyze_reviews(reviews)
stats = compute_statistics(analyzed)
print("Статистика:", stats)

export_results(analyzed, "output")
