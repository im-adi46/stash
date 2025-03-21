from .models import CustomUser, Calculation  
from django.core.mail import send_mail

def send_otp_email(email, otp):
    """Sends OTP email to the user."""
    send_mail(
        "Your OTP Code",
        f"Your OTP is: {otp}",
        'adityagawade.official46@gmail.com',
        [email],
        fail_silently=False,
    )
    print(f"Generated OTP for {email}: {otp}")
    
def handle_calculation(user, num1, num2, operation):
    result = None

    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'multi':
        result = num1 * num2
    elif operation == 'div':
        if num2 != 0:
            result = num1 / num2
        else:
            return "Error: Division by zero"

    calculation = Calculation.objects.create(
        user=user,
        num1=num1,
        num2=num2,
        operation=operation,
        result=result
    )

    return result
def get_users_by_operation(form):
    """Fetches users who performed a selected operation."""
    users, emails = [], []
    if form.is_valid():
        operation = form.cleaned_data["operation"]
        user_objects = Calculation.objects.filter(operation=operation).select_related("user").distinct()
        users = [user.user.username for user in user_objects]
        emails = [user.user.email for user in user_objects if user.user.email]
    return users, emails

def send_operation_notification(emails):
    """Sends email notification to users who performed an operation."""
    if emails:
        send_mail(
            "Notification: Operation Performed",
            "You have performed an operation on our platform.",
            'adityagawade.offical46@gmail.com',
            emails,
            fail_silently=False,
        )
        return True
    return False
