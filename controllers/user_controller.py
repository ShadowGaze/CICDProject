from flask import Blueprint, render_template, request, redirect, url_for
from models.user_model import get_all_users, create_user, delete_user
import json
from models.sales_model import (
    get_sales_by_month,
    get_sales_by_category,
    get_sales_trend,
    get_sales_by_region
)


user_bp = Blueprint('user', __name__)

# Show form to add a user


@user_bp.route('/', methods=['GET', 'POST'])
def add_user():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dob = request.form.get('dob', '').strip()
        email = request.form.get('email', '').strip()

        if not name or not dob or not email:
            error = 'All fields are required.'
        else:
            try:
                create_user(name, dob, email)
                return redirect(url_for('user.all_users'))
            except Exception as e:
                error = 'Email already exists or something went wrong.'

    return render_template('add_user.html', error=error)

# Show all users with delete button


@user_bp.route('/users')
def all_users():
    users = get_all_users()
    return render_template('users.html', users=users)


# Delete a user


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    delete_user(user_id)
    return redirect(url_for('user.all_users'))


@user_bp.route('/dashboard')
def dashboard():
    by_month = get_sales_by_month()
    by_category = get_sales_by_category()
    by_trend = get_sales_trend()
    by_region = get_sales_by_region()

    return render_template('dashboard.html',
                           bar_labels=json.dumps(by_month['labels']),
                           bar_values=json.dumps(by_month['values']),

                           pie_labels=json.dumps(by_category['labels']),
                           pie_values=json.dumps(by_category['values']),

                           line_labels=json.dumps(by_trend['labels']),
                           line_values=json.dumps(by_trend['values']),

                           doughnut_labels=json.dumps(by_region['labels']),
                           doughnut_values=json.dumps(by_region['values']),
                           )
