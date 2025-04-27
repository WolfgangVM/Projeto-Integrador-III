from itsdangerous import URLSafeTimedSerializer
from flask import current_app, Blueprint, request, url_for, flash, redirect, render_template
from flask_mailman import EmailMessage
from data.users import User
from extensions import db, bcrypt

forgot_password_bp = Blueprint('forgot_password', __name__)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email

@forgot_password_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            try:
                token = generate_reset_token(email)
                reset_url = url_for('forgot_password.reset_password', token=token, _external=True)
                msg = EmailMessage(
                    subject="Redefinição de Senha",
                    body=f"Olá, clique no link para redefinir sua senha: {reset_url}\n\nToken: {token}",
                    to=[email],
                )
                msg.send()
                flash('Um link para redefinir sua senha foi enviado para o seu e-mail, junto com o token.', 'info')
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")
                flash('Erro ao enviar o e-mail. Tente novamente mais tarde.', 'danger')
            return redirect(url_for('forgot_password.forgot_password'))
        else:
            flash('E-mail não encontrado.', 'danger')
            return redirect(url_for('forgot_password.forgot_password'))
    return render_template('EsqueciSenha.html')

@forgot_password_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('O link de redefinição de senha é inválido ou expirou.', 'danger')
        return redirect(url_for('forgot_password.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('senha')
        confirm_password = request.form.get('confirmar_senha')
        if new_password != confirm_password:
            flash('As senhas não coincidem. Tente novamente.', 'danger')
        else:
            user = User.query.filter_by(email=email).first()
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            flash('Sua senha foi redefinida com sucesso!', 'success')
            return redirect(url_for('login.loginpage'))
    
    return render_template('RecuperaSenha.html', token=token)