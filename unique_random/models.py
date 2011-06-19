from random import randrange

from django.contrib import admin
from django.db import models

# Example set is Crockford's encoding:
# http://www.crockford.com/wrmg/base32.html
CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
LENGTH = 16
MAX_TRIES = 1024

class UniqueRandom(models.Model):
    code = models.CharField(max_length=LENGTH, editable=False, unique=True)
    # Replace test_data with fields/relationships of choice.
    # Alternatively, copy the save() method and constants to another model.
    test_data = models.CharField("Test Data", max_length=128)
    
    class Meta:
        verbose_name = "Unique Random"
        verbose_name_plural = "Unique Randoms"
    
    def __unicode__(self):
        # Replace test_data here.
        return "%s: %s" % (self.code, self.test_data)
    
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
                for i in xrange(LENGTH):
                    new_code += CHARSET[randrange(0, len(CHARSET))]
                if not UniqueRandom.objects.filter(code=new_code):
                    self.code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        super(UniqueRandom, self).save(*args, **kwargs)

class UniqueRandomAdmin(admin.ModelAdmin):
    # Replace test_data here as well.
    list_display = ('code', 'test_data')
