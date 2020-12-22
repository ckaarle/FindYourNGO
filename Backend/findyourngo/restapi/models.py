from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

# strings should not be nullable, since in this case '' == null ?
# id: int PRIMARY KEY will be autogenerated for each class
# ManyToMany can be null by default, no need to explicitly declare it
from findyourngo.trustworthiness_calculator.trustworthiness_constants import TW_MIN_VALUE, TW_MAX_VALUE


class NgoBranch(models.Model):
    country = models.CharField(max_length=200)


class NgoTopic(models.Model):
    topic = models.CharField(max_length=200)


class NgoAccreditation(models.Model):
    accreditation = models.TextField()


class NgoDataSource(models.Model):
    credible = models.BooleanField()
    source = models.CharField(max_length=200)


class NgoMetaData(models.Model):
    last_updated = models.DateField(null=True)
    info_source = models.ManyToManyField(NgoDataSource)


class NgoAddress(models.Model):
    street = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)


class NgoRepresentative(models.Model):
    representative_first_name = models.CharField(max_length=200)
    representative_last_name = models.CharField(max_length=200)
    representative_email = models.EmailField()


class NgoContact(models.Model):
    ngo_phone_number = models.CharField(max_length=50)
    ngo_email = models.EmailField(null=True)
    website = models.CharField(max_length=200)
    address = models.ForeignKey(NgoAddress, null=True, on_delete=models.SET_NULL)
    representative = models.ForeignKey(NgoRepresentative, null=True, on_delete=models.SET_NULL)


class NgoType(models.Model):
    type = models.CharField(max_length=200)


class NgoStats(models.Model):
    founding_year = models.IntegerField(null=True)
    staff_number = models.IntegerField(default=0)
    member_number = models.IntegerField(default=0)
    working_languages = models.CharField(max_length=400)
    funding = models.CharField(max_length=200)
    president_first_name = models.CharField(max_length=200)
    president_last_name = models.CharField(max_length=200)
    type_of_organization = models.ManyToManyField(NgoType)
    yearly_income = models.CharField(max_length=200)


class NgoTWScore(models.Model):
    total_tw_score = models.FloatField(validators=[MinValueValidator(TW_MIN_VALUE), MaxValueValidator(TW_MAX_VALUE)])
    base_tw_score = models.FloatField(validators=[MinValueValidator(TW_MIN_VALUE), MaxValueValidator(TW_MAX_VALUE)])
    user_tw_score = models.FloatField(validators=[MinValueValidator(TW_MIN_VALUE), MaxValueValidator(TW_MAX_VALUE)])
    number_data_sources_score = models.FloatField(default=1)
    credible_source_score = models.FloatField(default=0)
    ecosoc_score = models.FloatField(default=0)


class Ngo(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=50)

    aim = models.TextField()
    activities = models.TextField()

    branches = models.ManyToManyField(NgoBranch)
    topics = models.ManyToManyField(NgoTopic)
    accreditations = models.ManyToManyField(NgoAccreditation)

    stats = models.ForeignKey(NgoStats, null=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey(NgoContact, null=True, on_delete=models.SET_NULL)

    meta_data = models.ForeignKey(NgoMetaData, on_delete=models.PROTECT) # meta data should not be deleted if a ngo is referencing them (we need the data source)
    tw_score = models.ForeignKey(NgoTWScore, on_delete=models.PROTECT)


class NgoCommenter(models.Model):
    user_id = models.IntegerField() # TODO change to foreign key of user table
    number_of_comments = models.IntegerField(default=0)


class NgoComment(models.Model):
    ngo_id = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    commenter_id = models.ForeignKey(NgoCommenter, on_delete=models.CASCADE)
    create_date = models.DateField()
    last_edited = models.DateField()
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(TW_MIN_VALUE), MaxValueValidator(TW_MAX_VALUE)])