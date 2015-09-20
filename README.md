django-unique-random
====================

Django model that generates unique random codes upon saving

Contact
-------

John J. Workman ([@workmajj](https://twitter.com/workmajj))

I worked on this software during my time as a [Recurse Center](https://www.recurse.com/) facilitator. If you'd like to join a warm community of programmers dedicated to self-improvement, you should consider applying. :-)

Description
-----------

While working on another project, I wanted to identify objects by codes that were:

* of a constant length;
* unique, though not necessarily universally;
* random (i.e., not generated from these objects' primary keys); and
* derived from a specific alphabet, in this case [Crockford's base-32 character set](http://www.crockford.com/wrmg/base32.html).

This Django app consists of a `models.py` file whose ```UniqueRandom``` model generates such codes. You can modify ```UniqueRandom``` to store other fields/relationships, but it's probably easier just to copy its ```save()``` method to one of your own models and sync/migrate your database.

The ```save()``` method works by making random codes of a given length. When a code is found that hasn't already been used, it's assigned to the current object. Obviously this method could be problematic for short codes and/or small alphabets; for a discussion, see [this Stack Overflow post](http://stackoverflow.com/questions/2076838/generating-non-repeating-random-numbers-in-python) (tl;dr: working with a base-10 alphabet, you're more than fine with 12-digit codes).

These codes work well as human-readable serial numbers that can be easily entered but not so easily guessed. **If you're interested in random-looking but deterministic IDs (and don't care about readability), try padding indexes then encrypting them with a symmetric algorithm.** You can then decrypt IDs, discard the padding, and use the plaintext indexes to look up rows quickly.

Thanks to [@diasgab](https://github.com/diasgab) for the Python 2-to-3 `xrange()`-to-`range()` update!

Testing & Usage
---------------

1. In a temporary directory, clone the GitHub repo:

        $ git clone git://github.com/workmajj/django-unique-random.git

2. Copy the `unique_random` app into your Django project directory.

3. If you're using Python 2 instead of 3, change `range()` (line 41 in `models.py`) to `xrange()`.

4. Add `'unique_random'` to your project's `settings.py` file:

        INSTALLED_APPS = (
            ...
            'unique_random'
        )

5. Migrate your database.

6. To test, log in to your project's admin interface and click on the Unique Randoms table. Add a few rows with dummy data in the ```test_data``` field. When you're finished, the rows (including unique random codes, which auto-generate) should look like this:

        PYHM90BKNF9DDKHC foo
        0QRGQQXKYYBQE92W bar
        XB2P12NMGS80FFNR baz
        G38D8R3R5M1S9Y5C qux

7. Now attach the ```UniqueRandom``` model in `models.py` to other data. You can replace ```test_data``` with your own fields, or set up relationships with other models. Actually, once you've tested this, it may be best just to copy the ```save()``` method (as well as its constants and ```code``` field) and add it to one of your existing models. In this case, you can remove the separate app.

8. Optionally, customize the codes by changing the alphabet (```CHARSET```) or the number of characters picked (```LENGTH```). If you do change these, make sure that ```MAX_TRIES``` is set to an appropriate value and that you handle possible ```ValueError``` exceptions.

License
-------

This code is in the public domain.
