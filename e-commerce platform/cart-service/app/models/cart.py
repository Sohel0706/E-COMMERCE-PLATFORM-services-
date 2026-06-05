from sqlalchemy import Column
from sqlalchemy import Integer

from app.database.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    product_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )
