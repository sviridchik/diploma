from .models import Guardian,Patient
def get_type_of_user(user):
    try:
        user.guardian
    except Guardian.DoesNotExist as e:
        try:
            user.patient
        except Patient.DoesNotExist as e:
            return "not found"
        return "patient"
    return "guardian"