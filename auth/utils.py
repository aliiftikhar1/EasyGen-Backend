# auth/utils.py
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def generate_verification_link(user, request):
    from django.urls import reverse

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    relative_link = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
    return request.build_absolute_uri(relative_link)
