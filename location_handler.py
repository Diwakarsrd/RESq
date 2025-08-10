from whatsapp import send_message

def handle_location(from_number, latitude, longitude):
    """
    Handle incoming location and send a response back via WhatsApp.
    """
    message = f"📍 Location received: {latitude}, {longitude}. Emergency team alerted!"
    send_message(from_number, message)
