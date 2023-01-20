def deploy():
    from app import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from models import User

    app = create_app()

    # application context is used to store data that is specific to the application,
    # such as the current configuration and the database object.
    # The push() method, makes it the current context.
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()


deploy()
