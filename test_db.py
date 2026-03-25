from database import init_db, save_bread, get_all_breads

init_db()

save_bread(
    notes="Test bread",
    feedback="Claude says it's good",
    image_path="test-bread.jpeg"
)

print(get_all_breads())