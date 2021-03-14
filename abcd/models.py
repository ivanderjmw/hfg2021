import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    

    def get_full_name(self):
        full_name: str = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_pk(self) -> str:
        output = self.email
        return ''.join(e for e in output if e.isalnum())


# All entities and associations are private to each user
# --------------------- Entities ------------------------
class Stakeholders(models.Model):
    name = models.TextField(
        blank = False
    )
    #Many-to-one user
    owner = models.ForeignKey(
        Profile,
        blank=False,
        on_delete=models.CASCADE
    )

class Tags(models.Model):
    name = models.TextField(
        blank=False
    )

class Assets(models.Model):
    name = models.TextField(
        blank=False
    )
    rating = models.SmallIntegerField()
    # class Meta:
    #     unique_fields = ('name', 'rating',)
    

class Institutions(models.Model):
    name = models.TextField(
        blank=False
    )
# --------------------- Relationships -------------------

class Strengths(models.Model):
    stakeholder = models.ManyToManyField(
        Stakeholders, related_name='s_stakeholder')
    tag = models.ManyToManyField(Tags, related_name='s_tag')

class Interests(models.Model):
    stakeholder = models.ManyToManyField(
        Stakeholders, related_name='i_stakeholder')
    tag = models.ManyToManyField(Tags, related_name='i_tag')

class Qualities(models.Model):
    stakeholder = models.ManyToManyField(
        Stakeholders, related_name='q_stakeholder')
    tag = models.ManyToManyField(Tags, related_name='q_tag')

class Owns(models.Model):
    stakeholder = models.ManyToManyField(Stakeholders, related_name="o_stakeholder")
    asset = models.ManyToManyField(Assets, related_name='o_asset')

class Possesses(models.Model):
    institution = models.ManyToManyField(Institutions, related_name='p_institution')
    asset = models.ManyToManyField(Assets, related_name='p_asset')

class Belongs(models.Model):
    institution = models.ManyToManyField(Institutions, related_name='b_institution')
    stakeholder = models.ManyToManyField(Stakeholders, related_name='b_stakeholder')
