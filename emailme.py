import smtplib, ssl

class EmailDetails: 
    def __init__ (self, from_email = "meghanolivia6@gmail.com", password = "bahubali"):
        self.port = 587
        self.smtp_server = "smtp.gmail.com" 
        self.sender_email = from_email
        self.password = password

    def send_message(self, message, receiver_email = "p.srijan08@gmail.com"):
        context = ssl.create_default_context()

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message)
        print("Successfully Sent Email...") 

    def basic_format_email (self, user, subject, body):
        message = """\
        Subject: %s 

        Hi %s your pick of the day is:
        %s """ % (subject , user, body) 
        return message
    
if __name__ == "__main__":
    m = EmailDetails()
    message = m.basic_format_email("Ram", "Testing", "Testing 123")
    m.send_message(message, "p.srijan08@gmail.com")