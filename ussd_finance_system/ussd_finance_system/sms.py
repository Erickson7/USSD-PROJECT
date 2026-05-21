import africastalking

username = "sandbox"

api_key = "atsk_95425448b131a2dde35a870999f079e6c047e01721f375f615914c22fe4b115066582696"

africastalking.initialize(
    username,
    api_key
)

sms = africastalking.SMS