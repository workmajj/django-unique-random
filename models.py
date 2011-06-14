# John J. Workman (@workmajj)
# django-random-code-model:
# A Django model that generates a unique random code upon saving.

from random import randrange

from django.contrib import admin
from django.db import models

# Example set is Crockford's encoding:
# http://www.crockford.com/wrmg/base32.html
CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
LENGTH = 8
MAX_TRIES = 1024

class RandomCode(models.Model):
    code = models.CharField(max_length=LENGTH, editable=False, unique=True)
    # Replace test_data with fields/relationships of choice.
    test_data = models.CharField("Test Data", max_length=128)
    
    class Meta:
        verbose_name = "Random Code"
        verbose_name_plural = "Random Codes"
    
    def __unicode__(self):
        return "%s: %s" % (self.code, self.test_data)
    
    def save(self, *args, **kwargs):
        """
        Upon saving, generate a random code by picking LENGTH number of
        characters from CHARSET and concatenating them. If code has already
        been used, repeat until a unique code is found, or fail after trying
        MAX_TRIES number of times. (This will work reliably for even modest
        values of LENGTH and MAX_TRIES, but do check for the exception.)
        """
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < MAX_TRIES:
                new_code = ''
                for i in xrange(LENGTH):
                    new_code = new_code + CHARSET[randrange(0, len(CHARSET))]
                if not RandomCode.objects.filter(code=new_code):
                    self.code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        super(RandomCode, self).save(*args, **kwargs)

class RandomCodeAdmin(admin.ModelAdmin):
    # Replace test_data here as well.
    list_display = ('code', 'test_data')
