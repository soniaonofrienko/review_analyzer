from src.core import load_reviews_from_csv

reviews = load_reviews_from_csv("data/sample_reviews.csv")
print(f"Было загружено {len(reviews)} отзывов")
for review in reviews[:3]:
    print(review)
