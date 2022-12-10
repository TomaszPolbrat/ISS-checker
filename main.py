import smtplib      # imports smtplib library
import time     # imports time library
from OOP_part import IssLocator     # imports IssLocator class
ISS_counter = 0     # ISS spotted counter
search = True   # beginning value for while loop
while search:
    time.sleep(30)      # time pause of 30 second between ISS location checks
    ISS = IssLocator()     # class item created
    if ISS.is_iss_visible():
        ISS_counter += 1        # adds 1 spotted event to counter
        if ISS_counter > 3:     # prevents email spam, because ISS will be visible for several minutes,
            # that means over 30 emails, this reduces it to 3 turning of the program
            search = False      # if 3 emails were send, this should close the while loop
        else:
            connect = smtplib.SMTP('64.233.184.108')    # Gmail SMTP address
            connect.starttls()      # connection action
            connect.login(user=ISS.my_email, password=ISS.password_app)     # loging in with credentials stated in OOP
            connect.sendmail(from_addr=ISS.my_email, to_addrs="YXZ@gmail.com",
                             msg="ISS nearby \n\n Check out the sky for ISS")  # email addresses of sender and receiver
            # and content of the email
            connect.close()     # closes the connection with Gmail server
