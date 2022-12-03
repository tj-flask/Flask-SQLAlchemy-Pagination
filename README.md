# flask-fast-pagination
Faster pagination using Seek method


## Usage

`model.py`
```py
class TestModel(db.Model):
    __tablename__ = "test_model"

    name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True, server_default=FetchedValue())
```

`api/test_model/view.py`

```py
from flask import Blueprint, jsonify, request
from flask_fast_pagination import Pagination


test_model_api = Blueprint("test_model_api", __name__, url_prefix="/api/test-models")

@test_model_api.route("/", methods=["GET"])
def list_():
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)

    query = TestModel.query.order_by(TestModel.name.asc())
    order_by = [TestModel.name]

    result = Pagination(
        model=TestModel,
        query=query,
        order_by_fields=order_by,
        page=page,
        per_page=per_page,
    )

    return jsonify({
        'page': result.page,
        'per_page': result.per_page,
        'total': result.total,
        'has_next': result.has_next,
        'has_prev': result.has_prev,
        'contract_vehicles': result.items,
    })
```
