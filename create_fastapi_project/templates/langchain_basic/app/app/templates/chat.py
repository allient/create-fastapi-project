chat_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title></title>
  </head>
  <body>
    <webchat-widget
      widget-websocket="ws://localhost:8000/api/v1/chat/tools"
      widget-color="#47A7F6"
      widget-chat-avatar="https://icon-library.com/images/ai-icon/ai-icon-7.jpg"
      widget-user-avatar="https://img2.freepng.es/20210721/osx/transparent-jedi-avatar-60f79d68da49c0.1144258416268404248941.jpg"
      widget-header="Bot"
      widget-subheader="Online"
      widget-placeholder="Send a message"
      widget-position="true"
      widget-on="false"
    >
    </webchat-widget>
    <script src="https://webchat-widget.pages.dev/static/js/main.js"></script>
  </body>
</html>
"""
