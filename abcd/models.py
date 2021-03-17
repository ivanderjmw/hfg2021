import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import JSONField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name="F", last_name="FF", password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin):
    """ Datamodel for user accounts. """
    email = models.EmailField(
        verbose_name='email address',
        max_length=127,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        unique=False,
        blank=False,
        max_length=127,
    )
    last_name = models.CharField(
        unique=False,
        blank=False,
        max_length=127,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    assocs = models.TextField()
    objects = MyUserManager()
    def get_full_name(self):
        full_name: str = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_pk(self) -> str:
        output = self.email
        return ''.join(e for e in output if e.isalnum())
    @property
    def is_staff(self):
        return True
    



# All entities and associations are private to each user
# --------------------- Entities ------------------------
class Node(models.Model):
    name = models.TextField(
        blank=False,
        unique=True
    )
    #Many-to-one user
    owner = models.ForeignKey(
        Profile,
        blank=True,
        # null=True,
        on_delete=models.CASCADE
    )
    x_coord = models.IntegerField(
        null=True
    )
    y_coord = models.IntegerField(
        null=True
    )

class Stakeholders(Node):
    def get_dict(self):
        d = dict()
        d["key"] = self.name
        d["color"] = "lightblue"
        return d

class Tags(Node):
    details = models.TextField(
        blank=True,
        null=True
    )
    magnitude = models.SmallIntegerField(
        null=True
    )
    def get_dict(self):
        d = dict()
        d["key"] = self.name
        d["color"] = "yellow"
        return d

#refering to physical asset not qualities like Kindness
class Assets(Node):
    details = models.TextField(
        blank=True,
        null=True

    )
    address = models.TextField(
        blank=True,
        null=True
    )
    contact = models.TextField(
        blank=True,
        null=True
    )

    def get_dict(self):
        if self.x_coord == None:
            d = dict()
            d["key"] = self.name
            d["color"] = "red"
            return d
        else:
            coord = str(self.x_coord) + " " + str(self.y_coord)
            d = dict()
            d["key"] = self.name
            d["color"] = "red"
            d["coord"] = coord
            return d
    

class Institutions(Node):
    details = models.TextField(
        blank=True,
        null=True
    )
    address = models.TextField(
        blank=True,
        null=True
    )
    contact = models.TextField(
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=127,
        blank=False,
        unique=False,
        null=True
    )

    def get_dict(self):
            d = dict()
            d["key"] = self.name
            d["color"] = "blue"
            return d


class Community(Node):
    location = models.TextField(
        blank=False
    )

    def get_dict(self):
        d = dict()
        d["key"] = self.name
        d["color"] = "yellow"
        return d

# --------------------- Relationships -------------------
# class Relationships(models.Model):
#     data = models.JSONField()
# class Associations(models.Model):
#     stakeholder1 = models.ManyToManyField(
#         Stakeholders, related_name='a_stakeholder1')
#     stakeholder2 = models.ManyToManyField(
#         Stakeholders, related_name='a_stakeholder2')

# class Strengths(models.Model):
#     stakeholder = models.ManyToManyField(
#         Stakeholders, related_name='s_stakeholder')
#     tag = models.ManyToManyField(Tags, related_name='s_tag')

# class Interests(models.Model):
#     stakeholder = models.ManyToManyField(
#         Stakeholders, related_name='i_stakeholder')
#     tag = models.ManyToManyField(Tags, related_name='i_tag')

# class Qualities(models.Model):
#     stakeholder = models.ManyToManyField(
#         Stakeholders, related_name='q_stakeholder')
#     tag = models.ManyToManyField(Tags, related_name='q_tag')

# class Owns(models.Model):
#     stakeholder = models.ManyToManyField(Stakeholders, related_name="o_stakeholder")
#     asset = models.ManyToManyField(Assets, related_name='o_asset')

# class Possesses(models.Model):
#     stakeholder = models.ManyToManyField(Institutions, related_name='p_stakeholder')
#     asset = models.ManyToManyField(Assets, related_name='p_asset')

# class Belongs(models.Model):
#     institution = models.ManyToManyField(Institutions, related_name='b_institution')
#     stakeholder = models.ManyToManyField(Stakeholders, related_name='b_stakeholder')
