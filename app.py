from flask import Flask, request, abort #架伺服器

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ySBWwAGG8avmdrorlSUKaR8vSWuxc+a4alcsPMa7qccfzZQjmBFOo+dU8K0PBAVagqVP5B4nM1dctWHaAKyN1nuAJJTBx9jyras4l1ww2Y9aF+Sb9kyI8o4XFkeayRtjpu53fpuex+TVWDluPCckigdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c64b24f6dfad46cfbd610edd3daf2c54')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()