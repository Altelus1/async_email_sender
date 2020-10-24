import asyncio
import aiosmtplib
import sys
import itertools


async def send_email_async(receiver, sender, mail_server):
    
    message = """From: <{}>
    To: <{}>
    Subject: Important
    MIME-Version: 1.0
    Content-type: text/html

    <b>Very Important!</b>
    <br />
    <a href="{http://important.local}">Click Here</a>
    """.format(sender, receiver)

    print("[*] Sending to: {}".format(receiver))
    try:
        await aiosmtplib.send(message, recipients=[receiver], sender=sendmail, hostname=mail_server,port= 25)         
        print("[+] Successfully sent email")
    except SMTPException as e:
        print("[-] Error: unable to send email: {}".format(e))



if __name__ == "__main__":
    
    emails_file = sys.argv[1]
    sender = sys.argv[2]
    mail_server = sys.argv[3]

    with open(emails_file, "r") as rf:
        users = rf.read().strip().split("\n")

    users = users[:25] # Depending on the server, sendin a lot of email might result in non-successful sending

    loop = asyncio.get_event_loop()

    args = [(user, mallink, sender) for user in users]
    tasks = itertools.starmap(send_email_async, args)
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
