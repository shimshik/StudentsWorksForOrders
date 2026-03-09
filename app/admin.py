from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from datetime import datetime
from app import db
from app.models import Shipment,ContactRequest

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    # Получаем фильтры из GET-запроса
    search_tracking = request.args.get('tracking', '').strip()
    filter_status = request.args.get('status', '').strip()
    filter_origin = request.args.get('origin', '').strip()
    filter_destination = request.args.get('destination', '').strip()

    # Начальный запрос
    query = Shipment.query

    # Применяем фильтры
    if search_tracking:
        query = query.filter(Shipment.tracking_number.like(f"%{search_tracking}%"))
    if filter_status:
        query = query.filter_by(status=filter_status)
    if filter_origin:
        query = query.filter(Shipment.origin.like(f"%{filter_origin}%"))
    if filter_destination:
        query = query.filter(Shipment.destination.like(f"%{filter_destination}%"))

    shipments = query.order_by(Shipment.last_update.desc()).all()
    return render_template('admin/dashboard.html', shipments=shipments)


@admin_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_shipment():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        status = request.form['status']
        tracking_number = request.form['tracking_number'].strip()

        if not tracking_number:
            flash("Трек-номер обязателен!", "error")
            return redirect(url_for('admin.add_shipment'))

        # Проверка на уникальность трек-номера
        existing = Shipment.query.filter_by(tracking_number=tracking_number).first()
        if existing:
            flash("Груз с таким трек-номером уже существует!", "error")
            return redirect(url_for('admin.add_shipment'))

        shipment = Shipment(
            origin=origin,
            destination=destination,
            status=status,
            tracking_number=tracking_number,
            last_update=datetime.utcnow()
        )
        db.session.add(shipment)
        db.session.commit()
        flash("Груз успешно добавлен!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/add_shipment.html')


@admin_bp.route('/update/<int:shipment_id>', methods=['GET', 'POST'])
@login_required
def update_shipment(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    if request.method == 'POST':
        shipment.origin = request.form['origin']
        shipment.destination = request.form['destination']
        shipment.status = request.form['status']
        shipment.last_update = datetime.utcnow()
        db.session.commit()
        flash("Груз обновлён!", "success")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/update_shipment.html', shipment=shipment)


@admin_bp.route('/delete/<int:shipment_id>', methods=['POST'])
@login_required
def delete_shipment(shipment_id):
    shipment = Shipment.query.get_or_404(shipment_id)
    tracking_number = shipment.tracking_number
    db.session.delete(shipment)
    db.session.commit()
    flash(f"Груз {tracking_number} успешно удален!", "success")
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы", "info")
    return redirect(url_for('main.index'))

@admin_bp.route('/contact-requests')
@login_required
def contact_requests():
    requests = ContactRequest.query.order_by(ContactRequest.created_at.desc()).all()
    return render_template('admin/contact_requests.html', requests=requests)

@admin_bp.route('/contact-requests/<int:request_id>/status', methods=['POST'])
@login_required
def update_request_status(request_id):
    contact_request = ContactRequest.query.get_or_404(request_id)
    status = request.form.get('status')
    if status in ['new', 'in_progress', 'completed']:
        contact_request.status = status
        db.session.commit()
        flash(f'Статус заявки обновлен', 'success')
    return redirect(url_for('admin.contact_requests'))