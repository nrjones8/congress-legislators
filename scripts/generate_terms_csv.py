import csv
import json
import glob
import os

import utils

yamls = ["legislators-current.yaml", "legislators-historical.yaml"]

def generate_terms(source_yaml_file):
    legislators = utils.load_data(source_yaml_file)
    num = 0

    # {'congress_num', 'start', 'end', }
    all_leg_terms = []
    for leg in legislators:
        num += 1
        bioguide_id = leg.get('id').get('bioguide')
        if bioguide_id is None:
            utils.log('No bioguide_id found for: ', leg)

        terms = leg.get('terms')

        for t in terms:
            start_of_term = utils.parse_date(t['start'])
            end_of_term = utils.parse_date(t['end'])
            # i.e. senator or representative
            office_type = t['type']

            congress_number = int(utils.congress_from_legislative_year(
                utils.legislative_year(start_of_term)
            ))

            all_leg_terms.append({
                'bioguide_id': bioguide_id,
                'office_type': office_type,
                'congress_number': congress_number,
                'start_date': start_of_term,
                'end_date': end_of_term,
            })

    write_leg_terms(all_leg_terms)
    

def write_leg_terms(list_of_term_dicts):
    field_names = list_of_term_dicts[0].keys()

    with open("../terms_served.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for term in list_of_term_dicts:
            writer.writerow(term)

    print('Finished writing out to ../terms_served.csv')
        

if __name__ == '__main__':
    generate_terms(yamls[1])