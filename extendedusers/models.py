import uuid
import logging

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

logger = logging.getLogger(__name__)

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    taxCode = models.CharField(max_length=100)
    personal_picture = models.ImageField(upload_to="images/", blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_tokens()
    
    def create_tokens(self):
        self.tokens.create()

    def set_verified(self):
        self.verified = True
        self.save()

class VerificationTokens(models.Model):
    """
    SO this will store the tokens/verificqation strings for each user"""

    account = models.ForeignKey(
        to=ExtendedUser, on_delete=models.CASCADE, related_name='tokens'
    )
    token = models.UUIDField(
        default=uuid.uuid4,
    )

    

    def send_token(self):
        subject = 'Verification Message'
        from_email = 'enricotroll91@gmail.com'
        to_email = self.account.user.email

        # we'll be using reverse_lazy coz we're not using the url right away.
        link = reverse_lazy('extended_users:verify', kwargs={
            'token_uuid': self.token, 'user_email': to_email,
        })

        context_data = {
            'name':  self.account.user.get_full_name(),
            'link': link,
        }
        plain_text = get_template('auth/verify.txt')
        text_content = plain_text.render(context_data)

        # print(str(text_content))

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.send()


    def save(self, *args, **kwargs):
        # So we will do the email logic here, when the token is saved. Bu in a real-life app you'd want this to run in the background
        # Which email backend are you using?
        # Its okay, we can use Mailhog, you know it?
        # Okay, so just download it, and we'll set thing up!


        

        # So now we just want to test if its sending mails be4 we proceed
        # you can run your migrations now
        # yes
        send_token = False
        if not self.pk:
            # I did this so that the token doesnt get send everytime the data is edited  since save is called on update and initial save. So django only gives a Model instance a `pk` after it is saved in the database, so if it doesnt have it, then its a new record.
            # yes

            send_token = True

        super().save(*args, **kwargs)

        if send_token:
            self.send_token()




