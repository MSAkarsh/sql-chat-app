from src.db import SessionLocal
from src.models import User, Post


def run():
    db = SessionLocal()

    # CREATE
    user = User(username="alice", email="alice@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    print("Created user:", user)

    post = Post(title="Hello World", body="First post", owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    print("Created post:", post)

    # READ
    users = db.query(User).all()
    print("All users:", users)

    # UPDATE
    user.username = "alice_updated"
    db.commit()
    print("Updated user:", user)

    # DELETE
    db.delete(post)
    db.commit()
    print("Deleted post", post.id)

    db.close()


if __name__ == "__main__":
    run()
