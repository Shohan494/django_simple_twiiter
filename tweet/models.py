# importing the dependencies
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# both of them are for django signals
# that creates an instance evrytime a new user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

# application users profile class
class UserProfile(models.Model):
    # the users will be unique, so one2one relation
    ## related name is used to point the model(the database table)
    ## to get all instances from this model(UserProfile):
    ## we have to write this "user.profile.all()"
    ## "User" field is imported from django provided "User" model
    ## and this field will be created as "user_id" in the db table
    user = models.OneToOneField(User, related_name='profile')

    # users relation will be many2many, so m2m relation
    # each user will have the ability to build a relationship
    # this relation table refers to the relation "through" the "Relation" model
    # users can follow another users, and slso can be followed by other users
    relation = models.ManyToManyField(
        # self is refering the UserProfile model
        # self refers to the same model class here it belongs to
        # 121,m2m,foreignkey relationships first argument is a model class
        'self',
        ## through means to which model this UserProfile model is connected
        ## here it is the "Relation" model
        ## that means the m2m relation is between UserProfile and Relation
        through='Relation',
        # it means "if an user follows someone, he is not following him"
        # one way, not both way(means not recursive)
        # and also the user can not follow himself
        symmetrical=False,
        related_name='related_to',
        default=None
    )

    # returns the full name of an user, built in function
    # about __unicode__: Django will call it when it needs to render an objects-
    # in a context where a string representation is needed
    # mostly used in admin section
    def __unicode__(self):
        return self.user.username

    # model methods defines row-based information
    # returns who is following the user
    def my_followers(self):
        return Relation.objects.filter(is_followed=self)

    # returns who the user is following
    def people_i_follow(self):
        return Relation.objects.filter(follower=self)

    # is called from the view to make a row entry to the db
    # generally it makes a query and then saves the data to db
    # this(get_or_create) also doesn't return querysets
    def follow(self, person_to_follow):
        # this relation is an object that holds the data
        relation, created = Relation.objects.get_or_create(
            follower=self,
            is_followed=person_to_follow
        )
        return relation

    #
    def unfollow(self, person_to_unfollow):
        try:
            Relation.objects.get(
                follower=self,
                is_followed=person_to_unfollow
            ).delete()
        except Relation.DoesNotExist:
            pass
        return

# If the source and target models differ, the following fields are generated:
# 1. id: the primary key of the relation.
# 2. <containing_model>_id: the id of the model that declares the ManyToManyField.
# 3. <other_model>_id: the id of the model that the ManyToManyField points to.

## here the ForeignKeys are important issues
## as a m2m relationship, this "Relation" models fields(follower and is_followed) are-
## related to the "user_id" field from the "UserProfile" model
class Relation(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follows')
    is_followed = models.ForeignKey(UserProfile, related_name='followers')
    follow_time = models.DateTimeField(auto_now_add=True)

    # defines who is following who
    # in admin section it will be viewed
    def __unicode__(self):
        return '%s follows %s' % (self.follower.user.username, self.is_followed.user.username)

    # meta classes of django provides extra information
    # the relationship of following must be unique
    class Meta:
        unique_together = ('follower', 'is_followed')

# To make sure that every new user gets his user profile instance created
# this is called django signals, by this we can have a row inserted everytime-
# an user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
