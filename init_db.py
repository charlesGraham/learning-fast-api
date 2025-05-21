import database
import models


def init_db():
    models.Base.metadata.create_all(bind=database.engine)
    database.engine.dispose()


if __name__ == "__main__":
    init_db()
