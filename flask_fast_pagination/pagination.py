from dataclasses import dataclass
from functools import cached_property
from typing import List

from flask_sqlalchemy import BaseQuery
from math import ceil
from sqlakeyset import get_page, Page

from server.extensions import db


@dataclass
class Pagination:
    query: BaseQuery
    model: db.Model
    per_page: int
    order_by_fields: List[db.Column]
    page: int

    @cached_property
    def pages(self) -> int:
        return ceil(self.total / self.per_page)

    @cached_property
    def _page(self) -> Page | List:
        last_record = (
            self.query
            .with_entities(*self.order_by_fields)
            .limit(1)
            .offset(abs(self.per_page * (self.page - 1) - 1)).first()
        )

        if last_record:
            page = (tuple(getattr(last_record, c.key) for c in self.order_by_fields), False)
            return get_page(self.query, per_page=self.per_page, page=page)

        return []

    @property
    def items(self) -> Page:
        return self._page

    @property
    def has_prev(self) -> bool:
        return self._page.paging.has_previous if self.page else False

    @property
    def has_next(self) -> bool:
        return self._page.paging.has_next if self.page else False

    @property
    def total(self) -> int:
        return self.query.order_by(None).count()
