from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from extensions import db, bcrypt
from data.users import User


forgot_password_bp = Blueprint('forgot_password', __name__)

@forgot_password_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Armazena o e-mail na sessão para usá-lo na próxima etapa
            session['reset_email'] = email
            flash('Um link para redefinir sua senha foi enviado para o seu e-mail.', 'info')
            return redirect(url_for('forgot_password.reset_password'))
        else:
            flash('E-mail não encontrado.', 'danger')
            return redirect(url_for('forgot_password.forgot_password'))
    return render_template('EsqueciSenha.html')

@forgot_password_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = session.get('reset_email')  # Recupera o e-mail armazenado na sessão
    if not email:
        flash('Sessão expirada. Tente novamente.', 'danger')
        return redirect(url_for('forgot_password.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('senha')
        confirm_password = request.form.get('confirmar_senha')
        if new_password != confirm_password:
            flash('As senhas não coincidem. Tente novamente.', 'danger')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()
                flash('Sua senha foi redefinida com sucesso!', 'success')
                session.pop('reset_email', None)  # Remove o e-mail da sessão
                return redirect(url_for('login.login'))
            else:
                flash('Usuário não encontrado. Tente novamente.', 'danger')
                return redirect(url_for('forgot_password.forgot_password'))
    return render_template('RecuperaSenha.html')