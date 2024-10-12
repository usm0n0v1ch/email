import uuid

def generate_confirmation_token():
    return str(uuid.uuid4())
