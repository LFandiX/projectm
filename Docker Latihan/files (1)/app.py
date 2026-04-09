import os, logging
from datetime import timedelta
from flask import Flask, session
from config import Config
from services.db import close_db, init_db

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(days=30)
    
    # Teardown
    app.teardown_appcontext(close_db)
    
    # Blueprints
    from routes.auth import bp as auth_bp
    from routes.dashboard import bp as dashboard_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    # Template filters
    import humanize
    @app.template_filter('filesize')
    def filesize_filter(n):
        if n is None: return '0 B'
        return humanize.naturalsize(n, binary=True)
    
    @app.template_filter('datetime')
    def datetime_filter(dt):
        if dt is None: return '-'
        return dt.strftime('%d %b %Y, %H:%M')
    
    @app.template_filter('reltime')
    def reltime_filter(dt):
        if dt is None: return '-'
        import humanize as h
        from datetime import datetime, timezone
        return h.naturaltime(dt)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
