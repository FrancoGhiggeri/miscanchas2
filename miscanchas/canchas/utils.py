import string
import random
from .models import Reserva

def generate_unique_code():
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(random.choices(characters, k=13))    
    try:
        codigo_operacion = Reserva.objects.get(codigo_operacion=unique_code)
        return generate_unique_code()
    except:
        return unique_code
