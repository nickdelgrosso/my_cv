__author__ = 'nicholas'

import yaml
from collections import defaultdict
from cv_preamble import *

doc = get_cv_doc('docs/delgrosso_cv')

def build_section(cv_doc, data, section_name, formatter):
    cv_doc.append(SubHeading(section_name))
    for entry in data[section_name]:
        entry = defaultdict(str, entry) if isinstance(entry, dict) else entry
        cv.append(formatter(entry))

def build_section_itemized(cv_doc, data, section_name, item_formatter):
    cv_doc.append(SubHeading(section_name))
    for entry in data[section_name]:
        with doc.create(Itemize()) as itemize:
            itemize.add_item(item_formatter(entry))

def format_skill_item(entry):
    return bold(entry) + NoEscape(': ') + NoEscape(', '.join(data[section][entry]))

def format_goals_item(entry):
    return entry

def format_research(entry):
    return NewEntry([' -\n  '.join([entry['StartDate'], entry['EndDate']]),
                     entry['Institute'],
                     entry['Supervisor'],
                     entry['Description']
                    ])

def format_industry(entry):
    return NewEntry([' -\n '.join(entry['StartDate', entry['EndDate']]),
                     entry['Position'],
                     entry['Institute'],
                     entry['Description']
                    ])

def format_conference_pub(entry):
    return NewEntry([entry['Date'],
                     entry['Conference'],
                     entry['Title'],
                     entry['Description']
                    ])

def format_journal_pubs(entry):
    return Description(entry)

def format_awards(entry):
    return DescMarg([entry['Date'], entry['Title']])

def format_education(entry):
    return NewEntry([entry['Date'], entry['Degree'], entry['Institute'], ''])

def format_personal(entry):
    for key, value in entry.items():
        if 'mail' in key:
            value = Email(value)
        return HeaderOnly([key, value])

with doc.create(CV(arguments='Nicholas A. Del Grosso')) as cv:

    # Space between title and the first section
    cv.append(vspace('2em'))

    with open('research_experiences.yaml') as f:

        data = yaml.load(f)

        for section in ['Personal Info', 'Goals', 'Education', 'Research Experience', 'Industry Experience',
                        'Journal Publications', 'Conference Publications', 'Skills', 'Awards']:

            # Section Data
            if section == 'Personal Info':
                build_section(cv, data, 'Personal Info', format_personal)

            elif section == 'Research Experience':
                build_section(cv, data, 'Research Experience', format_research)

            elif section == 'Industry Experience':
                build_section(cv, data, 'Industry Experience', format_industry)

            elif section == 'Journal Publications':
                build_section(cv, data, 'Journal Publications', format_journal_pubs)

            elif section == 'Conference Publications':
                build_section(cv, data, 'Conference Publications', format_conference_pub)

            elif section == 'Skills':
                build_section_itemized(cv, data, 'Skills', format_skill_item)

            elif section == 'Goals':
                build_section_itemized(cv, data, 'Goals', format_goals_item)

            elif section == 'Awards':
                build_section(cv, data, 'Awards', format_awards)

            elif section == 'Education':
                build_section(cv, data, 'Education', format_education)

    # Add a signature at the bottom
    cv.append(includegraphics(options='width=5cm', arguments='images/Signaturetransparant.png'))


doc.generate_pdf()
doc.generate_tex()