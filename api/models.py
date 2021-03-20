from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import  make_password


# Create your models here.

class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    nbr_students = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=320, blank=True, null=True)
    mode = models.BooleanField(default=False)

    class Meta:
        db_table = 'api_school'


    def __str__(self):
        return self.id


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    school_id = models.ForeignKey('School', on_delete=models.CASCADE)
    class_field = models.CharField(db_column='class', max_length=10, blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        db_table = 'api_student'

    def __str__(self):
        return self.id


class Subscription(models.Model):
    id_school = models.ForeignKey('School', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    payed = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'api_subscription'
    
    def __str__(self):
        return self.id_school


class Transfer(models.Model):
    id_transfer = models.AutoField(primary_key=True)
    id_student = models.ForeignKey('Student', on_delete=models.CASCADE)
    from_school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='transfert_from')
    to_school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='transfert_to')
    demand_date = models.DateField(blank=True, null=True)
    transfer_date = models.DateField(blank=True, null=True)
    validation_to = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'api_transfer'


class Observation(models.Model):
    id_student= models.ForeignKey('Student', on_delete=models.CASCADE)
    observation = models.TextField(blank=True, null=True)
    teacher = models.CharField(max_length=50, blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'api_observation'



class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email, firstname, lastname, function, school, password=None):
        """Creates a new user profile object."""

        if not email:
            raise ValueError('Users must have a email address.')

        if not firstname:
            raise ValueError('Users must have a firstname.')

        if not lastname:
            raise ValueError('Users must have a lastname.')

        if not school:
            raise ValueError('Users must have a school.')

        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, function=function, school=school)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email,  firstname, lastname, school, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email,  firstname, lastname, "admin", school, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a 'user profile' inside our system """


    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    function = models.CharField(max_length=25, blank=True)
    school = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname','school']

    def get_full_name(self):
        """Get user full name """
        return self.firstname + self.lastname

    def get_short_name(self):
        """Get user short name """

        return self.firstname

    def __str__(self):
        """Django uses this when it needs to convert the object as a string """
        return self.email

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles' 
        db_table = 'api_profile'

