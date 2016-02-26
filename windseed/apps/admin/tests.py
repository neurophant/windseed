import tornado.testing

from windseed.base.test import Test
from windseed.apps.admin.models import User


class UserTestCase(Test):
    @tornado.testing.gen_test
    def test(self):
        user = User.create(email='email@email.com', password='password1')
        self.assertIsInstance(user, User)
        uid = user.uid
        equal = user.check_password(password='password1')
        self.assertEqual(equal, True)

        updated = User.update(password='password2')\
            .where(User.uid == uid)\
            .execute()
        self.assertEqual(updated, 1)
        user = User.get(User.uid == uid)
        equal = user.check_password(password='password2')
        self.assertEqual(equal, True)

        user.password = 'password3'
        saved = user.save()
        self.assertEqual(saved, 1)
        user = User.get(User.uid == uid)
        equal = user.check_password(password='password3')
        self.assertEqual(equal, True)

        user.delete_instance()
