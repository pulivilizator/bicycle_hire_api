from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, patronymic=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            patronymic=patronymic,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user