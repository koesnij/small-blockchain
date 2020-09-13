from flask import Flask

from app.views import ViewInjector

view_injector = ViewInjector()


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return 'Hello Flask!!'

    view_injector.init_app(app)

    return app


app_ = create_app()
