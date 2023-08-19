import json, os

from flask import request
from flask_restful import Resource
import requests

from models import db, User

WHATSAPP_API_ENDPOINT = os.environ["WHATSAPP_API_ENDPOINT"]
WHATSAPP_API_KEY = os.environ["WHATSAPP_API_KEY"]


class IncomingMessageWebhook(Resource):
    """_summary_

    Payload => {
        "id": "true_919997747930@s.whatsapp.net_3EB0997A8934D1DFC414",
        "channelId": 12070,
        "receiverNumber": "919997747930",
        "senderNumber": "9193291031066",
        "senderName": "You",
        "itemType": "buttons_response",
        "boundType": "out",
        "value": "OK",
        "time": 1659717319000,
    };

    Args:
        Resource (_type_): _description_
    """

    def post(self):
        payload = request.get_json()
        if payload["boundType"] != 'out':
            return {"message": "success"}, 200

        if payload["itemType"] != "buttons_response":
            return {"message": "success"}, 200

        user = db.session.query(User).filter(User.channel_id == payload["channelId"]).first()
        if user is None:
            return {"message": "Channel is not registered!"}, 421

        request_payload = {
            "title": "Catalogue ",
            "body": "WhatsApp Plans",
            "footer": "",
            "filePath": "WA_Plans_5_May_2023.pdf",
            "fileType": "DOCUMENT",
            "templateButtons": [
                {
                "type": "URL_BUTTON",
                "displayText": "Visit Website",
                "value": "https://sites.google.com/sheetomatic.in/intranet/home",
                },
                { "type": "CALL_BUTTON", "displayText": "Call Back", "value": "9329103106" },
                { "type": "QUICK_REPLY_BUTTON", "displayText": "Interested", "value": "Text" },
            ],
        }

        # We can add invisible unicode character in the button texts that can help us identify
        # the action taken by the user. The following two functions will allow to perform the same
        #
        # ord()
        # chr()

        response = requests.post(
            "https://app.messageautosender.com/api/v1/message/create",
            data=json.dumps(request_payload),
            headers={"Content-Type": "applcation/json", "x-api-key": WHATSAPP_API_KEY}
        )
        response.raise_for_status()
        return {"message": "success"}, 200

