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
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;
                     color: #333;">
            <h2 style="color: #4CAF50;">📩 Nova Mensagem de Contato</h2>
            <p><strong>Nome:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Telefone:</strong> {phone}</p>
            <p><strong>Mensagem:</strong></p>
            <p style="margin-left: 20px; font-style: italic;">"{message}"</p>
            <hr>
            <p style="font-size: 12px; color: #777;">
                Recebido via formulário do site MoneyWise
            </p>
        </body>
        </html>
        """

        try:
            msg = Message(
                subject='Nova mensagem de contato',
                recipients=[
                    'joaomarcos.jm@ges.inatel.br'
                ],
                html=email_body
            )
            mail.send(msg)
            return redirect(url_for('home.home_page'))
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return redirect(url_for('home.contact_page'))

    return render_template('contact.html')
