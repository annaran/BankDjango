import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    # Function to connect to the websocket

    def connect(self):

       # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            self.group_name = "notifications"
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name)
            print("group name", self.group_name)

            self.accept()
    # Function to disconnet the Socket

    def disconnect(self, close_code):
        self.close()
        pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))


class NotificationTransferConsumer(WebsocketConsumer):

    def connect(self):

        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.group_name = str(self.scope["user"].pk)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name)
            print("group name", self.group_name)
            self.accept()

    def disconnect(self, close_code):
        self.close()
        pass

    def notifyAboutTransfer(self, event):
        self.send(text_data=json.dumps(event["text"]))
