from flask import Blueprint, render_template

home = Blueprint(
    'home',
    __name__,
    static_url_path='',
    template_folder='templates',
    static_folder='static'
)

@home.route('/')
def home_page():
    return render_template('home.html')

@home.route('/login')
def login_page():
    return render_template('login.html')  # Certifique-se de ter esse arquivo
