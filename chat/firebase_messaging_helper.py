import requests
import json

fbMessagingUrl = "https://fcm.googleapis.com/fcm/send"

headers = {
    "Authorization": "key=AAAAVyhsIL4:APA91bHk-dLFAziaRNQVWpuhdCAwAGvbi1O-FITSGbvNvkNA7tPSHpzQUUJpL43hU0Vpri2OO_YFBNUBCdEQ012HeXQR2p9gH_Od1SOKjF2AdBZiPCQoPmN9VRkK-EyOBvVb0-X5vfpr",
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
            'notificationData': notificationData,
        },
        "to": "/topics/userId%d" % userId
    })

    response = requests.post(
        fbMessagingUrl,
        data=data,
        headers=headers,
    )

    print(response.text)


# pushNotification(
#     userId=2,
#     title='Brahim',
#     body='message',
#     notificationData={'brahim': 'chouih'},
# )
