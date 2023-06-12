from django.core.exceptions import ValidationError

def validate_work_day(value):
    try:
        if value.weekday == 5 or value.weekday==6:
            raise ValidationError(f"{value}  is not a work day! You are allowed to update only during working days!" )
    except Exception as e:
        raise ValidationError(f"OOPS! error occured! -->  {e} ")
def validate_phone(value):
    if len(value) > 10 or len(value) < 10:
        raise ValidationError('Phone number should have 10 digits!')
    