from django.core.mail import send_mail


def email_message(message_dict):
    contents = f"""
   Hi, thank you for trying to reset your password.
   click: {message_dict['reset-link']}
   """
    send_mail(
        'Password Reset Link',
        contents,
        'martanetza2210@gmail.com',
        [message_dict['email_reveiver']],
        fail_silently=False
    )
