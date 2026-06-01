from app.models.user import User


def create_user(db, user_data):

    user = User(
        name=user_data.name,
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db):
    return db.query(User).all()


def get_user(db, user_id):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )