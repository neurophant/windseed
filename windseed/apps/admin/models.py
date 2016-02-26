import crypt
import hmac

import peewee

from windseed.base.model import Model


class User(Model):
    """
    User db model:
        active - is user active and can he authenticate
        superuser - is user a superuser

        email - user email
        phash - password hash
    """
    active = peewee.BooleanField(default=False, index=True)
    superuser = peewee.BooleanField(default=False)

    email = peewee.CharField(max_length=256, unique=True, index=True)
    phash = peewee.CharField(max_length=256)

    class Meta:
        indexes = (
            (('active', 'email', ), True, ), )

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Update password hash on create
        """
        if 'password' in kwargs.keys():
            kwargs['phash'] = crypt.crypt(kwargs.pop('password'),
                                          crypt.mksalt())

        return super().create(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        """
        Update password hash on update
        """
        if 'password' in kwargs.keys():
            kwargs['phash'] = crypt.crypt(kwargs.pop('password'),
                                          crypt.mksalt())

        return super().update(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Update password hash on save
        """
        if getattr(self, 'password', None) is not None:
            self.phash = crypt.crypt(self.password, crypt.mksalt())
            del self.password

        return super().save(*args, **kwargs)

    def check_password(self, password=None):
        """
        Check password
        """
        return hmac.compare_digest(self.phash,
                                   crypt.crypt(password, self.phash))
