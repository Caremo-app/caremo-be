# Importing the Required Library
import pywhatkit

# Defining the Phone Number and Message
phone_number = "+6285345871185"
message = "awikwok"

# Sending the WhatsApp Message
pywhatkit.sendwhatmsg_instantly(phone_number, message, 15, True)


# Displaying a Success Message
print("WhatsApp message sent!")