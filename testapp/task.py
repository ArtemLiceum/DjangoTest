from background_task import background
from django.core.mail import send_mail


@background()
def send_shop_update_email(shop_id: int, email: str) -> None:
    subject = "Обновление магазина"
    message = f"Магазин с ID {shop_id} был обновлён"
    from_email = "bedintema@gmail.com"

    send_mail(subject, message, from_email, [email])
