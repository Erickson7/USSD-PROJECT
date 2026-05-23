

import africastalking

import os

username = os.environ.get("sandbox")

api_key = os.environ.get("atsk_dfb618ea70a52e2ee01dc7854112e3af8a203346f0ee3949eb69d2b8e6b34c6dbe3b0f2f")


if not username or not api_key:
    print("⚠️ Africa's Talking credentials missing!")
    username = "sandbox"
    api_key = "dummy_key"

africastalking.initialize(username, api_key)


sms = africastalking.SMS