from datetime import datetime
from app.models.testroute import Items

def test_item_creation_defaults():
    now = datetime.utcnow()
    item = Items(title="unit_test", description="testing", createdAt=now)
    assert item.title == "unit_test"
    assert isinstance(item.createdAt, datetime)