from app import app
from models import Portfolio


if __name__ == "__main__":
    port = int(app.config.get("SERVER_PORT", 5000))
    with app.app_context():
        print(f"instance_path={app.instance_path}")
        print(f"db_uri={app.config.get('SQLALCHEMY_DATABASE_URI')}")
        try:
            print(f"portfolio_count={Portfolio.query.count()}")
        except Exception as exc:
            print(f"startup_db_error={exc!r}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
