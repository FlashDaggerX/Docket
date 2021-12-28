#!/usr/bin/env python
"""Generates the secrets.py file for Django"""
LOCATION = "Docket/secrets.py"


def main():
    try:
        from django.core.management.utils import get_random_secret_key
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        file = open(LOCATION, mode='w')
        file.write("SECRET_KEY = \"{}\"\n".format(get_random_secret_key()))
        file.flush()
    finally:
        file.close()


if __name__ == '__main__':
    main()
