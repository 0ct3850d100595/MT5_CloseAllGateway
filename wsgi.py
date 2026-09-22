import os

from app import create_app

app = create_app(
    phone_token=os.environ.get("PHONE_TOKEN", ""),
    ea_token=os.environ.get("EA_TOKEN", ""),
)
