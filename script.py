import re
import json


def sanitize_phone_number(phone_number):
    phone_number = phone_number.replace(' ', '')
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(')', '')
    phone_number = phone_number.replace('(', '')
    return phone_number


def validate_phone_number(phone_number):
    sanitized = sanitize_phone_number(phone_number)
    if len(sanitized) == 10:
        return True
    return False


def normalize_phone_number(phone_number):
    sanitized = sanitize_phone_number(phone_number)
    normailzed = '%s-%s-%s' % (sanitized[:3], sanitized[3:6], sanitized[6:])
    return normailzed


def process_lines(lines):
    out = dict()
    out['entries'] = list()
    out['errors'] = list()
    for count, line in enumerate(lines):
        candidate = line.rfind(',')
        last_word = line[candidate+2:] if candidate > -1 else ''
        user = dict()
        fields = line.split(',')
        if re.match('^(\d{5})$', last_word):
            # zip code format is Lastname, Firstname,
            # (703)-742-0996, Blue, 10013
            user_keys = ['lastname', 'firstname', 'phonenumber', 'color',
                         'zipcode']
            for i, key in enumerate(user_keys):
                user[key] = fields[i].rstrip()
        elif re.match('^([a-z])', last_word):
            # color format is Firstname, Lastname, 10013, 646 111 0101, Green
            user_keys = ['firstname', 'lastname', 'zipcode', 'phonenumber',
                         'color']
            for i, key in enumerate(user_keys):
                user[key] = fields[i].rstrip()
        else:
            # phone format is Firstname Lastname, color, 10013, 646 111 0101
            if len(fields) > 1:
                sanatize_field = fields[0]
                first = sanatize_field[:sanatize_field.rfind(' ')]
                last = sanatize_field[sanatize_field.rfind(' ')+1:]
                user['firstname'] = first
                user['lastname'] = last
                remaining_keys = ['color', 'zipcode', 'phonenumber']
                for i in range(1, 4):
                    key = remaining_keys[i-1]
                    user[key] = fields[i].rstrip()
        if user and validate_phone_number(user['phonenumber']):
            user['phonenumber'] = normalize_phone_number(user['phonenumber'])
            out['entries'].append(user)
        else:
            out['errors'].append(count)
    return out


def main():
    processed_output = None
    with open('data.in', 'r') as f:
        processed_output = process_lines(f)
    if processed_output is not None:
        with open('result.out', 'w') as outfile:
            json.dump(processed_output, outfile, sort_keys=True,
                      indent=2)
    else:
        print 'looks like something broke...'

if __name__ == "__main__":
    main()
