from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаём объект БД глобально, чтобы импортировать в моделях
db = SQLAlchemy()

def create_app():
    """Фабрика Flask-приложения."""
    app = Flask(__name__)

    # --- Конфигурация ---
    app.config['SECRET_KEY'] = 'any-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Инициализация расширений ---
    db.init_app(app)

    # --- Регистрация маршрутов ---
    from app.routes import main
    app.register_blueprint(main)

    # --- Создание таблиц при первом запуске ---
    with app.app_context():
        db.create_all()

    return app