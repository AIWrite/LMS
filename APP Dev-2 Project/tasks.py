from app import celery_app
from mailer import mail as email
from flask_mail import Message
from taskcontext import ContextTask
from models import db, User, Book
from datetime import date, timedelta
from flask import send_file
import csv

@celery_app.task(base=ContextTask)
def test():
    return "x"

@celery_app.task(base=ContextTask)
def mailuserlogin():
    email_subject = "Visit back if you liked us."
    email_body = "Your books are missing you. Visit them today to know a new story."
    today = date.today()
    users = User.query.all()
    for user in users:
        if user.last_login_at.date() < today:
            print(user.email)
            format = "<html><body>"
            format += "<h1>Hi, " + user.username + "</h1>"
            format += "<p>" + email_body + "</p>"
            format += "</body></html>"
            msg = Message(subject=email_subject, recipients=[user.email])
            msg.body = email_body
            msg.html = format
            email.send(msg)
        else:
            pass

@celery_app.task(base=ContextTask)
def mailuserbooks():
    email_subject = "Return Date Near"
    email_body = "Books return date is approaching. Kindly return it before 7 days or else the librarian will have to revoke the access."
    day_after_tomorrow = date.today() + timedelta(days=2)
    books = Book.query.all()
    for book in books:
        if (book.return_at != None) and (book.return_at.date() == day_after_tomorrow):
            print(book.user_email)
            format = "<html><body>"
            format += "<h1>Hi, " + book.username + "</h1>"
            format += "<h1>For Book:, " + book.name + "</h1>"
            format += "<p>" + email_body + "</p>"
            format += "</body></html>"
            msg = Message(subject=email_subject, recipients=[book.user_email])
            msg.body = email_body
            msg.html = format
            email.send(msg)
        else:
            pass

    return 'ok'

@celery_app.task(base=ContextTask)
def maillib():
    email_subject = "Monthly Report"
    email_body = "Following is the montly report for the library management system."
    users = User.query.all()
    books = Book.query.all()
    format = "<html><body>"
    format += "<h1>Hi Librarian</h1>"
    format += "<p>" + email_body + "</p>"
    format += "<p>Books Details</p>"
    format += '<table><tr><th>Name</th><th>Authors</th><th>Description</th><th>Created-On</th><th>Updated-On</th>th>Requested-Granted</th><th>Returned-Revoked</th><th>Issued-Status</th><th>Section-Category</th><th>Issued-To</th><th>User-MailID</th><th>Rating</th><th>Issued-On</th><th>Revoke-Date</th></tr>'
    for book in books:
        format += '<tr><td>'+ book.name + '</td><td>' + book.authors + '</td><td>' + book.description + '</td><td>' + str(book.created_at) + '</td><td>' + str(book.updated_at) + '</td><td>' + str(book.requested) + '</td><td>' + str(book.returned) + '</td><td>' + str(book.status) + '</td><td>' + str(book.section_name) + '</td><td>' + str(book.username) + '</td><td>' + str(book.user_email) + '</td><td>' + str(book.like) + '</td><td>' + str(book.issued_at) + '</td><td>' + str(book.return_at) + '</td></tr>'
    format += '</table>'

    format += "<p> </p>"

    format += "<p>Users Details</p>"
    format += '<table><tr><th>Name</th><th>Email</th><th>Granted-Requested</th><th>Revoked-Returned</th><th>Last-Login</th><th>Login-Count</th></tr>'
    for user in users:
        format += '<tr><td>' + user.username + '</td><td>' + user.email + '</td><td>' + str(user.granted) + '</td><td>' + str(user.revoked) + '</td><td>' + str(user.last_login_at) + '</td><td>' + str(user.login_count) + '</td></tr>'
    format += '</table>'
    format += "</body></html>"
    msg = Message(subject=email_subject, recipients=['lib@a.com'])
    msg.body = email_body
    msg.html = format
    email.send(msg)
    return 'ok'

@celery_app.task(base=ContextTask)
def export_ebooks_to_csv():
    books = Book.query.all()
    csv_file = 'books.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Author(s)', 'Created Date', 'Updated Date', 'Requested/Granted', 'Returned/Revoked', 'Issue Status', 'Section', 'Issued to (User)', 'User eMail', 'Rating', 'Issued Date', 'Return Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()                                                                                                                                                                                                                 
        for book in books:
            writer.writerow({
                'Name': book.name,
                'Author(s)': book.authors,
                'Created Date': book.created_at,
                'Updated Date': book.updated_at,
                'Requested/Granted':  book.requested,
                'Returned/Revoked': book.returned,
                'Issue Status': book.status, 
                'Section': book.section_name, 
                'Issued to (User)': book.username, 
                'User eMail': book.user_email, 
                'Rating': book.like,
                'Issued Date': book.issued_at,
                'Return Date': book.return_at
            })
    return send_file(csv_file)


# @celery_app.task(base=ContextTask)
# def mail():
#     email_subject = "Test Email"
#     email_body = "This is a test email"
#     users = User.query.all()
#     for user in users:
#         print(user.email)
#         format = "<html><body>"
#         format += "<h1>Hi, " + user.username + "</h1>"
#         format += "<p>" + email_body + "</p>"
#         format += "</body></html>"
#         msg = Message(subject=email_subject, recipients=[user.email])
#         msg.body = email_body
#         msg.html = format
#         email.send(msg)
#     return 'ok'