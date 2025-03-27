from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include user.pk, timestamp, and user.is_active status in the hash
        return str(user.pk) + str(timestamp) + str(user.is_active)


# Create an instance of the token generator
account_activation_token = AccountActivationTokenGenerator()
