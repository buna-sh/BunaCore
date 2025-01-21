# routes/home.py
def init_app(app):
    @app.route('/')
    def home():
        return 'Welcome to the Home Page!'
