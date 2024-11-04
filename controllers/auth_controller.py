from datetime import *
from flask import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mail import Mail, Message
from models.models import *

def register_acc(s, mail):
    data = request.get_json()
    email = data.get('email')
    user = Users.query.filter_by(email=email).first()

    if user:
        return jsonify({'message': 'Email already exists'}), 400

    new_user = Users(
        name=data.get('name'),
        email=email,
        address=data.get('address'),
        phone_number=data.get('phone_number'),
        img_profile='https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y',
        roles_id=data.get('roles_id'),
        is_verified=False
    )
    new_user.set_password(data.get('password'))

    db.session.add(new_user)
    db.session.commit()

    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)
    msg = Message('Confirm Your Email', sender='admin@agrolyn.online', recipients=[email])
    msg.body = f'Please click the link to verify your email: {confirm_url}'
    mail.send(msg)

    return jsonify({'message': 'User registered. Check email to confirm account.'}), 201

def confirm_email_acc(token, s):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), 400

    user = Users.query.filter_by(email=email).first()
    if user.is_verified:
        return jsonify({'message': 'Account already confirmed.'}), 400
    else:
        user.is_verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified. You can now log in.'}), 200
    
def login_acc():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Users.query.filter_by(email=email).first() 

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    if not user.is_verified:
        return jsonify({'message': 'Email not verified'}), 403

    access_token = create_access_token(identity={'id': user.id,'email': user.email, 'name': user.name})
    session['logged_in'] = True
    return jsonify({'access_token': access_token}), 200

def forgot_pwd(s, mail):
    data = request.get_json()
    email = data.get('email')
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Email not found'}), 404

    token = s.dumps(email, salt='reset-password')
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', sender='admin@agrolyn.online', recipients=[email])
    msg.body = f'Please click the link to reset your password: {reset_url}'
    mail.send(msg)

    return jsonify({'message': 'Password reset email sent'}), 200

def reset_pwd(token, s):
    if request.method == 'GET':
        return jsonify({'message': 'Success verify email reset password.'}), 200

    elif request.method == 'POST':
        # Coba memuat email dari token
        try:
            email = s.loads(token, salt='reset-password', max_age=3600)
        except:
            return jsonify({'message': 'The reset link is invalid or has expired.'}), 400

        data = request.get_json()
        user = Users.query.filter_by(email=email).first()
        
        # Cek jika user ditemukan
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Setel ulang password
        user.set_password(data.get('new_password'))
        db.session.commit()
        return jsonify({'message': 'Password has been reset successfully'}), 200


def logout_acc():
    session.pop('logged_in', None)
    return jsonify({'message': 'Logged out successfully'}), 200