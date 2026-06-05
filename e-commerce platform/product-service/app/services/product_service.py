from app.models.product import Product


def create_product(db, product_data):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db):
    return db.query(Product).all()


def get_product(db, product_id):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )
