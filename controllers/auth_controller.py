from datetime import *
from flask import *
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_mail import Message
from models.models import *

def refresh_token():
    identity = get_jwt_identity()  # Mendapatkan identitas pengguna dari refresh token
    new_access_token = create_access_token(identity=identity)  # Membuat access token baru

    return jsonify({
        'access_token': new_access_token
    }), 200

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
        img_profile='https://ui-avatars.com/api/?name=' + data.get('name') + '&background=random',
        roles_id=data.get('roles_id'),
        is_verified=False
    )
    new_user.set_password(data.get('password'))

    db.session.add(new_user)
    db.session.commit()

    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('confirm_email', token=token, _external=True)

    # HTML email template
    html = render_template_string('''
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <!-- Logo Section -->
            <div style="text-align: center; padding-bottom: 10px;">
                <img src="https://agrolyn.online/static/assets/favicon.png" alt="Agrolyn Logo" style="width: 80px; height: 80px;">
            </div>
            
            <!-- Header Section -->
            <div style="background-color: #4CAF50; padding: 10px 20px; border-radius: 8px 8px 0 0; color: #ffffff; text-align: center;">
                <h2 style="margin: 0;">Welcome to Agrolyn!</h2>
            </div>
            
            <!-- Body Content -->
            <div style="padding: 20px;">
                <p>Hi {{ name }},</p>
                <p>Thank you for registering with Agrolyn. Please confirm your email address by clicking the button below:</p>
                <p style="text-align: center;">
                    <a href="{{ confirm_url }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Confirm Email</a>
                </p>
                <p>If the button above doesn't work, copy and paste the following link into your browser:</p>
                <p style="word-break: break-all; color: #555;"><a href="{{ confirm_url }}">{{ confirm_url }}</a></p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="font-size: 12px; color: #777;">If you did not register for an Agrolyn account, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    ''', name=data.get('name'), confirm_url=confirm_url)

    msg = Message('Confirm Your Email', sender='AGROLYN <admin@agrolyn.online>', recipients=[email])
    msg.html = html
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

    # Buat access token dan refresh token
    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'roles_id': user.roles_id
    })
    refresh_token = create_refresh_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'roles_id': user.roles_id
    })
    
    session['logged_in'] = True

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'address': user.address,
        'phone_number': user.phone_number,
        'img_profile': user.img_profile,
        'roles_id': user.roles_id
    }), 200

def forgot_pwd(s, mail):
    data = request.get_json()
    email = data.get('email')
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Email not found'}), 404

    token = s.dumps(email, salt='reset-password')
    reset_url = url_for('reset_password', token=token, _external=True)

    # HTML template for the email
    html = render_template_string('''
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <!-- Logo Section -->
            <div style="text-align: center; padding-bottom: 10px;">
                <img src="https://agrolyn.online/static/assets/favicon.png" alt="Agrolyn Logo" style="width: 80px; height: 80px;">
            </div>

            <!-- Header Section -->
            <div style="background-color: #4CAF50; padding: 10px 20px; border-radius: 8px 8px 0 0; color: #ffffff; text-align: center;">
                <h2 style="margin: 0;">Reset Your Password</h2>
            </div>
            
            <!-- Body Content -->
            <div style="padding: 20px;">
                <p>Hello,</p>
                <p>You requested a password reset for your account. Please click the button below to set a new password:</p>
                <p style="text-align: center;">
                    <a href="{{ reset_url }}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a>
                </p>
                <p>If the button above doesn't work, copy and paste the following link into your browser:</p>
                <p style="word-break: break-all; color: #555;"><a href="{{ reset_url }}">{{ reset_url }}</a></p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="font-size: 12px; color: #777;">If you did not request this, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    ''', reset_url=reset_url)

    msg = Message('Password Reset Request', sender='AGROLYN <admin@agrolyn.online>', recipients=[email])
    msg.html = html
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