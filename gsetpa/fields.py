import pycountry
from django.db import models

countries = list(
    map(
        lambda country: (
            country.alpha_2,
            country.name,
        ),
        pycountry.countries,
    )
)
currencies = list(
    map(
        lambda currency: (
            currency.alpha_3,
            currency.name,
        ),
        pycountry.currencies,
    )
)


class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["choices"] = countries
        return super().__init__(*args, **kwargs)


class CurrencyField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["choices"] = currencies
        return super().__init__(*args, **kwargs)
