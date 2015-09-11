from random import randrange

from django.contrib import admin
from django.db import models

# example charset is crockford's encoding:
# http://www.crockford.com/wrmg/base32.html

CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
LENGTH = 16
MAX_TRIES = 32

# replace test_data below (marked with TODO) with fields of choice
# alternatively, copy save() method and constants to another model

class UniqueRandom(models.Model):
    code = models.CharField(max_length=LENGTH, editable=False, unique=True)
    test_data = models.CharField("Test Data", max_length=128) # TODO: test_data

    class Meta:
        verbose_name = "Unique Random"
        verbose_name_plural = "Unique Randoms"

    def __unicode__(self):
        return "%s: %s" % (self.code, self.test_data) # TODO: test_data

    def save(self, *args, **kwargs):
        """
        Upon saving, generate a code by randomly picking LENGTH number of
        characters from CHARSET and concatenating them. If code has already
        been used, repeat until a unique code is found, or fail after trying
        MAX_TRIES number of times. (This will work reliably for even modest
        values of LENGTH and MAX_TRIES, but do check for the exception.)
        Discussion of method: http://stackoverflow.com/questions/2076838/
        """
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < MAX_TRIES:
                new_code = ''
                for i in range(LENGTH): # TODO: change to xrange() for python 2
                    new_code += CHARSET[randrange(0, len(CHARSET))]
                if not UniqueRandom.objects.filter(code=new_code):
                    self.code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        super(UniqueRandom, self).save(*args, **kwargs)

class UniqueRandomAdmin(admin.ModelAdmin):
    list_display = ('code', 'test_data') # TODO: test_data
