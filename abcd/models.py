import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import JSONField

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
    def get_full_name(self):
        full_name: str = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_pk(self) -> str:
        output = self.email
        return ''.join(e for e in output if e.isalnum())



# All entities and associations are private to each user
# --------------------- Entities ------------------------
class Node(models.Model):
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
    name = models.TextField(
        blank = False
    )
    def get_dict(self):
        return {"key": self.name, "color": "lightblue"},

class Tags(Node):
    name = models.TextField(
        blank=False
    )
    details = models.TextField(
        blank=True
    )
    magnitude = models.SmallIntegerField()
    def get_dict(self):
        return {"key": self.name, "color": "yellow"},

#refering to physical asset not qualities like Kindness
class Assets(Node):
    name = models.TextField(
        blank=False
    )
    details = models.TextField(
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    contact = models.TextField(
        blank=True
    )
    rating = models.FloatField()

    def get_dict(self):
        return {"key": self.name, "color": "red"},
    

class Institutions(Node):
    name = models.TextField(
        blank=False
    )
    details = models.TextField(
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    contact = models.TextField(
        blank=True
    )
    site = models.TextField(
        blank=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=127,
        blank=False,
        unique=False,
    )
    rating = models.SmallIntegerField()

    def get_dict(self):
        return {"key": self.name, "color": "blue"},


class Community(Node):
    location = models.TextField(
        blank=False
    )

    def get_dict(self):
        return {"key": self.name, "color": "yellow"},

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
