from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


# Class [UserManager] : Customize User Model
class UserManager(BaseUserManager):

    # FUNC [create_user] : To create normal user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            content = {'msg': 'Email address should not be empty', 'response_status': 'Failed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_active = True;
        user.admin = False;
        user.staff = False;
        user.is_deActive = False;
        user.set_password(password)
        user.save(using=self.db)
        return user

    # FUNC [create_superuser] : To create super user
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.admin = True
        user.staff = True
        user.save(using=self.db)
        return user


# Class [User] : Define attributes for user model
class User(AbstractBaseUser):
    # define choices
    GENDER_OPTIONS = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    NATIONALITY_OPTIONS = (('Nepalese', 'Nepalese'), ('Japanese', 'Japanese'), ('Chinese', 'Chinese'))
    # define attributes
    full_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=15, choices=NATIONALITY_OPTIONS, default="Nepalese")
    citizenship_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    cover_pic = models.ImageField(null=True, blank=True)
    government_pic = models.ImageField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS, default="Male")
    age = models.IntegerField(null=True, blank=True)
    mobileNo = models.CharField(max_length=20, null=True, blank=True)
    secondaryNo = models.CharField(max_length=20, null=True, blank=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deActive = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    email = models.EmailField(verbose_name="email", max_length=80, unique=True)
    password = models.CharField(max_length=50)
    # create an instance of user manager
    objects = UserManager()
    # required field while creating new user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have specific permission?"""
        return True;

    def has_module_perms(self, app_label):
        """Does user have permission to view app level ?"""
        return True;

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def tokens(self):
        refreshToken = RefreshToken.for_user(self)
        return {
            'refresh': str(refreshToken),
            'access': str(refreshToken.access_token)
        }
