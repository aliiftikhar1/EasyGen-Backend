from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']  # For createsuperuser

    def __str__(self):
        return self.email


class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fine_tune_description = models.TextField(blank=True, null=True)
    modify_post_cta = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Preferences"

class ContentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class PostingGoal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class WritingStyle(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class JobDescription(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class UserPreferenceSelection(models.Model):
    user_preference = models.ForeignKey(UserPreference, on_delete=models.CASCADE)
    content_types = models.ManyToManyField(ContentType, blank=True)
    posting_goals = models.ManyToManyField(PostingGoal, blank=True)
    writing_styles = models.ManyToManyField(WritingStyle, blank=True)
    industries = models.ManyToManyField(Industry, blank=True)
    job_descriptions = models.ManyToManyField(JobDescription, blank=True)


    def __str__(self):
        return f"Selections for {self.user_preference.user.email}"

class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    BILLING_CHOICES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.package.name} ({self.billing_cycle})"

    def save(self, *args, **kwargs):
        # Auto-calculate end_date based on billing cycle if not provided
        if not self.end_date:
            if self.billing_cycle == 'monthly':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.billing_cycle == 'yearly':
                self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)