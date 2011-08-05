django-unique-random
====================

A Django model that generates a unique random code upon saving.

Contact
-------

John J. Workman ([@workmajj](https://twitter.com/workmajj))

Description
-----------

While working on another project, I wanted to identfiy objects by codes that were:

* of a constant length;

* unique, though not universally;

* random, i.e. not generated from these objects' primary keys;

* derived from a specific alphabet, in this case [Crockford's](http://www.crockford.com/wrmg/base32.html) base-32 character set.

This Django app consists of a models.py file whose ```UniqueRandom``` model generates such codes. You can modify ```UniqueRandom``` to store other fields/relationships, but it's probably easier to just copy its ```save()``` method to one of your own models and sync/migrate your database.

The ```save()``` method works by generating random codes of a certain length. When a code is found that hasn't already been used, it's assigned to the current object. Obviously this method is not foolproof and could be problematic for short codes and/or small alphabets. For a discussion, see this Stack Overflow article on [Generating non-repeating random numbers in Python](http://stackoverflow.com/questions/2076838/generating-non-repeating-random-numbers-in-python). (tl;dr: With a base-10 alphabet, you're more than fine with 12-digit codes.)

These ended up working well as human-readable serial numbers that could be easily entered and not so easily guessed.

Testing & Usage
---------------

1. In a temporary directory, clone the GitHub repo:

        $ git clone git://github.com/workmajj/django-unique-random.git

2. Copy the unique_random app into your current Django project directory.

3. Add unique_random to your project's settings.py file:

        INSTALLED_APPS = (
            ...
            'unique_random'
        )

4. Sync your database or migrate if using South.

5. To test, log in to your project's admin interface and click on the Unique Randoms table. Add a few rows with dummy data in the ```test_data``` field. When you're finished, the rows (including unique random codes, which auto-generate) should look something like this:

        PYHM90BKNF9DDKHC foo
        0QRGQQXKYYBQE92W bar
        XB2P12NMGS80FFNR baz
        G38D8R3R5M1S9Y5C qux

6. Now attach the ```UniqueRandom``` model in models.py to other data. You can replace ```test_data``` with fields of your choice, or set up relationships with other models. Actually, once you've tested that this works, it may be best to just copy the ```save()``` method (as well as its constants and ```code``` field) and add it to one of your existing models. In this case, you can remove the separate app from your project and database.

7. Customize the codes by changing the set ```CHARSET``` from which characters are chosen, or the number of characters ```LENGTH``` that are picked. (If you do change these, make sure that ```MAX_TRIES``` is set to an appropriate value and that you handle the possible ```ValueError``` exception.)

8. Profit!

License
-------

This code is in the public doman.
