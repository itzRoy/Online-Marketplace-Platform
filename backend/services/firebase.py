import firebase_admin
from firebase_admin import credentials, storage

from backend.config import settings


class FirebaseStorage:
    def __init__(self):

        creds = {
            "type": settings.FIREBASE_TYPE,
            "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "project_id": str(settings.FIREBASE_PROJECT_ID),
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            # this key took me almost an hour to figure out
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace(r"\n", "\n"),
            "client_email": str(settings.FIREBASE_CLIENT_EMAIL),
            "client_id": str(settings.FIREBASE_CLIENT_ID),
            "token_uri": str(settings.FIREBASE_TOKEN_URI),
            "auth_uri": str(settings.FIREBASE_AUTH_URI),
            "client_x509_cert_url": str(
                settings.FIREBASE_CLIENT_X509_CERT_URL
            ),
            "universe_domain": str(settings.FIREBASE_UNIVERSE_DOMAIN),
        }

        credentials_certificate = credentials.Certificate(creds)

        firebase_admin.initialize_app(
            credentials_certificate,
            {"storageBucket": settings.FIREBASE_STORAGE_BUCKET},
        )

        self.bucket = storage.bucket()

    async def upload_image_to_firestore(self, image_file):
        blob = self.bucket.blob(image_file.filename)
        image = await image_file.read()
        blob.upload_from_string(image, content_type=image_file.content_type)
        blob.make_public()
        return blob.public_url


firebase_storage = FirebaseStorage()
