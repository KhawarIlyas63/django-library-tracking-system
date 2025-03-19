from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned = False, due_date__lt = now())

    subject = "Overdue Book Loan Reminder"
    for loan in overdue_loans:
        member_email = loan.member.user.email
        member_name = f"{loan.member.user.first_name} {loan.member.user.last_name}".strip()
        book_title = loan.book.title
        messaage = f"Dear {member_name},\n\nYour book '{book_title}' is overdue. Please return it as soon as possible."
        send_mail(
            subject=subject,
            message=messaage,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    print(f'Sent {overdue_loans.count()} overdue loans notifications.')
