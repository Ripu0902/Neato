"""
Module: tasks.py

This module contains Celery tasks for sending reminder messages to inactive users
and monthly reports to active users via email. It also includes setup for periodic tasks.

Functions:
    - send_reminder_webhooks(): Sends reminder messages to inactive users via webhook.
    - send_monthly_reports(): Sends monthly reports to active users via email.
    - setup_intervalTASK(): Sets up periodic tasks for reminders and reports.

"""

import os
import csv, io, time
from datetime import datetime, timedelta
import requests
from collections import defaultdict
from app import celery
from application.database import Professional, Service_request, ServiceStatus, Customer
from jinja2 import Template
from weasyprint import HTML
from application.mail_config import send_email
from sqlalchemy import and_
from application.config import LocalDevelopementConfig

@celery.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs):
    sender.add_periodic_task(
        # Send a remainder at 5:30pm IST of every day
        # crontab(minute=30, hour=17),
        60,
        send_reminder_webhooks.s(),
        name="Daily reminder",
    )

    sender.add_periodic_task(
        # Send the monthly report at 5:30pm IST of every month
        # crontab(minute=3 , hour=20),
        10,
        send_monthly_reports.s(),
        name="Monthly Report",
    )


@celery.task(name="tasks.send_reminder_webhooks")
def send_reminder_webhooks():
    """
    Send reminder messages to inactive users via webhook.

    This function retrieves inactive users from the database and sends them reminder
    messages via a specified webhook URL.

    Parameters:
        None

    Returns:
        None
    """
    yesterday = datetime.now() - timedelta(days=1)
    
    inactive_users = Professional.query.filter(Professional.last_seen <= yesterday).all()

    # Dictionary to store the number of reminders sent to each user
    reminders_sent_count = defaultdict(int)

    for user in inactive_users:
        if user.last_seen is None:
            continue  # Skip users without activity data

        # Define the maximum number of reminders allowed for each user
        max_reminders = 3  # Adjust this value as needed

        # Check if the maximum number of reminders has been reached for this user
        if reminders_sent_count[user.professional_id] >= max_reminders:
            continue  # Skip sending reminders to this user

        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAtSuQAZk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ZyDE0RGqI221sFnnlkVYnlKDYOaSfzRbEfONoANSahM'  # Update with your actual webhook URL
        payload = {
            "text": f"Heyy {user.fullname} it's been a day. We are missing you. we might have a treat for you XO",
        }

        response = requests.post(webhook_url, json=payload, timeout=10)
        print(response.status_code)
        if response.status_code == 200:
            reminders_sent_count[
                user.professional_id
            ] += 1  # Increment the reminders sent count for this user
            print("Success")



@celery.task()
def send_monthly_reports():
    """Send monthly activity reports to customers."""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background: #2E8B57; color: white; padding: 20px; }
            .content { padding: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Monthly Activity Report - {{ month_year }}</h1>
            <p>Report for: {{ customer_name }}</p>
        </div>
        <div class="content">
            <h2>Service Summary</h2>
            <p>Total Services: {{ total_services }}</p>
            <p>Completed Services: {{ completed_services }}</p>
            <p>Average Rating: {{ avg_rating }}</p>
            
            <h2>Service Details</h2>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Service</th>
                    <th>Professional</th>
                    <th>Status</th>
                    <th>Rating</th>
                </tr>
                
                <tr>
                    <td>Heyy its from jimmy </td>
                    <td>{{ service.name }}</td>
                    <td>{{ service.professional }}</td>
                    <td>{{ service.status }}</td>
                    <td>{{ service.rating }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    '''

    try:
        month_start = datetime.now().replace(day=1)
        last_month = month_start - timedelta(days=1)
        last_month_start = last_month.replace(day=1)

        customers = Customer.query.all()
        reports_sent = 0

        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        for customer in customers:
            services = Service_request.query.filter(and_(
                Service_request.customer_id == customer.customer_id,
                Service_request.date_of_request.between(last_month_start, last_month)
            )).all()

            if not services:
                continue

            service_list = []
            total_rating = 0
            rated_count = 0

            for service in services:
                professional = Professional.query.get(service.professional_id)
                if service.ratings:
                    total_rating += service.ratings
                    rated_count += 1

                service_list.append({
                    'date': service.date_of_request.strftime('%Y-%m-%d'),
                    'name': professional.service_type,
                    'professional': professional.fullname if professional else 'Unknown',
                    'status': service.service_status.value,
                    'rating': service.ratings or 'N/A'
                })

            data = {
                'customer_name': customer.fullname,
                'month_year': last_month.strftime('%B %Y'),
                'total_services': len(services),
                'completed_services': len([s for s in services if s.service_status == ServiceStatus.COMPLETED]),
                'avg_rating': f"{total_rating/rated_count:.1f}" if rated_count else 'N/A',
                'services': service_list
            }

            html_content = Template(template).render(**data)
            
            # Generate PDF with a unique filename
            pdf_filename = f'report_{customer.customer_id}_{int(time.time())}.pdf'
            pdf_path = os.path.join(reports_dir, pdf_filename)
            
            # Generate PDF with optimized settings
            HTML(string=html_content).write_pdf(
                pdf_path,
                optimize_size=('fonts', 'images')
            )

            try:
                # Send email with PDF attachment
                send_email(
                    to=customer.email,
                    subject=f'Monthly Activity Report - {last_month.strftime("%B %Y")}',
                    msg=html_content,
                    attachment=pdf_path
                )
                reports_sent += 1
            except Exception as email_error:
                print(f"Failed to send email to {customer.email}: {str(email_error)}")
                # Keep the PDF if email fails
                continue

        return {'status': 'success', 'message': f'Generated and sent {reports_sent} reports'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}



