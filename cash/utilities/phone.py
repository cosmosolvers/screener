import phonenumbers


def phone_number(phone):
    phone = phonenumbers.parse(phone, None)
    if not phonenumbers.is_valid_number(phone):
        raise ValueError('Invalid phone number')
    return phone


def get_country_code(phone):
    phone = phone_number(phone)
    return phonenumbers.region_code_for_number(phone)


def get_country(phone):
    phone = phone_number(phone)
    return phonenumbers.geocoder.description_for_number(phone, 'en')
