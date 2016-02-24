import tornado.testing

from windseed import base, models


class UserTestCase(base.Test):
    @tornado.testing.gen_test
    def test(self):
        user = models.User.create(email='email@email.com',
                                  password='password1')
        self.assertIsInstance(user, models.User)
        uid = user.uid
        equal = user.check_password(password='password1')
        self.assertEqual(equal, True)

        updated = models.User.update(password='password2')\
            .where(models.User.uid == uid)\
            .execute()
        self.assertEqual(updated, 1)
        user = models.User.get(models.User.uid == uid)
        equal = user.check_password(password='password2')
        self.assertEqual(equal, True)

        user.password = 'password3'
        saved = user.save()
        self.assertEqual(saved, 1)
        user = models.User.get(models.User.uid == uid)
        equal = user.check_password(password='password3')
        self.assertEqual(equal, True)

        user.delete_instance()
