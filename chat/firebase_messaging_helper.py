import requests
import json

fbMessagingUrl = "https://fcm.googleapis.com/fcm/send"

headers = {
    "Authorization": "key=AAAA4lm4s_w:APA91bGRuvN6Ffk6aJ-2RzG9IUjv1u4oqY6GXCA7N42bJhf6ksN7Po5Wmt1idPYrYoRFaHUC2LWr3Te70bS1YByvRgNoDos-8gU2nWSerAz0zrvrDq93xMBy6Yk69gnRfPQjvP_HKWNT",
    "Content-Type": "application/json",
}


def pushNotification(title='', body='', userId='', notificationData={}):
    data = json.dumps({
        "notification": {
            "title": title,
            "body": body,
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
        },
        "data": {
            'messageData':notificationData,
        },
        "to": "/topics/userEkrili%d" % userId
    })

    response = requests.post(
        fbMessagingUrl,
        data=data,
        headers=headers,
    )

    print(response.text)


# pushNotification(
#     userId=5,
#     title='Brahim',
#     body='message',
#     notificationData={
#         'brahim': 'chouih',
#         'id':322,
#     },
# )
