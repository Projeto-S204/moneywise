from flask import Blueprint, render_template, request, redirect, url_for
from flask_mail import Message
from config import mail

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

@home.route('/informations')
def informations_page():
    return render_template('informations.html')

@home.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        # Capturar os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        mensagem = request.form.get('mensagem')

        corpo_email = f"""
        Nova mensagem de contato:

        Nome: {nome}
        Email: {email}
        Telefone: {telefone}
        Mensagem: {mensagem}
        """

        try:
            msg = Message(subject='Nova mensagem de contato',
                          recipients=['lauraschiavon00@gmail.com'],  # Troque pelo email de destino
                          body=corpo_email)
            mail.send(msg)
            return redirect(url_for('home.sucesso'))
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return 'Erro ao enviar email'

    return render_template('contact.html')

@home.route('/sucesso')
def sucesso():
    return 'Email enviado com sucesso!'
