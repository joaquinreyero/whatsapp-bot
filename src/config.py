import os


class Settings:
    def __init__(self):
        self.PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
        self.ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        self.APP_ID = os.getenv("APP_ID")
        self.APP_SECRET = os.getenv("APP_SECRET")
        self.RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
        self.VERSION = os.getenv("VERSION")
        self.PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


settings = Settings()
