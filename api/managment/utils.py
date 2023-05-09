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

def token_to_code(token: str) -> str:
    res = 0
    secret = 67
    for c in token:
        res *= secret
        res += ord(c)
    return str(res)[-6:]