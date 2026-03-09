from flask import Blueprint, render_template, request,flash
from app.models import Shipment,ContactRequest
from app import db


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/track', methods=['POST'])
def track():
    tracking_number = request.form.get('tracking_number')
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    return render_template('track_result.html', shipment=shipment)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/cases')
def cases():
    return render_template('cases.html')

@main_bp.route('/offices')
def offices():
    return render_template('offices.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not all([name, email, phone, message]):
            flash('Пожалуйста, заполните все поля', 'error')
            return render_template('contact.html')

        contact_request = ContactRequest(
            name=name,
            email=email,
            phone=phone,
            message=message,
            status='new'
        )

        try:
            db.session.add(contact_request)
            db.session.commit()
            flash('Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка. Пожалуйста, попробуйте позже.', 'error')

        return render_template('contact.html')

    return render_template('contact.html')


