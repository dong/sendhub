import json
import phonenumbers
from exception import RequestParameterError

MESSAGE_REQUIRED_FIELDS = ["message", "recipients"]

class MessageFactory(object):
    @staticmethod
    def validate_fields(data_dict, required_keys):
        for key in required_keys:
            if key not in data_dict:
                raise RequestParameterError("Invalid request parameter: %s is not included" % key)
    @staticmethod
    def validate_recipients_size(data_dict):
        size = len(data_dict.get("recipients", []))
        if not size:
            raise RequestParameterError("Invalid recipient size: at least 1 recipients")

    @staticmethod
    def validate_phonenumbers(phone_numbers):
        for pnumber in phone_numbers:
            try:
                phone_number = phonenumbers.parse(pnumber, "US")
                valid = phonenumbers.is_valid_number(phone_number)
            except:
                valid = False
            finally:
                if not valid:
                    raise RequestParameterError("Invalid phone number: %s" % pnumber)

    @staticmethod
    def create_message(request_data):
        data_dict = json.loads(request_data)
        MessageFactory.validate_fields(data_dict, MESSAGE_REQUIRED_FIELDS)
        MessageFactory.validate_recipients_size(data_dict)
        MessageFactory.validate_phonenumbers(data_dict['recipients'])
        msg = MessageSchema()
        msg.message = data_dict["message"]
        msg.recipients = list(set(data_dict["recipients"]))
        return msg

class MessageSchema(object):
    def __init__(self):
        self.message = ""
        self.recipients = []

    def to_dict(self):
        return {"message": self.message,
                "recipients": str(self.recipients)
                }

    def __str__(self):
        return str(self.to_dict())

