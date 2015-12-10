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

with doc.create(CV(arguments='Nicholas A. Del Grosso')) as cv:

    # Space between title and the first section
    cv.append(vspace('2em'))

    with open('research_experiences.yaml') as f:

        data = yaml.load(f)

        for section in ['Personal Info', 'Goals', 'Education', 'Research Experience', 'Industry Experience',
                        'Journal Publications', 'Conference Publications', 'Skills', 'Awards']:

            # Section Title
            cv.append(SubHeading(section))

            # Section Data
            if section == 'Personal Info':
                for key, value in data[section].items():
                    if 'mail' in key:
                        value = Email(value)
                    cv.append(EntryHeader(['', key, value]))
                    cv.append(NoEscape(r'\\'))

            elif section == 'Research Experience':
                build_section(cv, data, 'Research Experience', format_research)

            elif section == 'Industry Experience':
                build_section(cv, data, 'Industry Experience', format_industry)

            elif section == 'Journal Publications':
                build_section(cv, data, 'Journal Publications', format_journal_pubs)

            elif section == 'Conference Publications':
                build_section(cv, data, 'Conference Publications', format_conference_pub)

            elif section == 'Skills':
                with doc.create(Itemize()) as itemize:
                    for entry in data[section]:
                        itemize.add_item(bold(entry) + NoEscape(': ') + NoEscape(', '.join(data[section][entry])))

            elif section == 'Goals':
                for entry in data[section]:
                    with doc.create(Itemize()) as itemize:
                        itemize.add_item(entry)

            elif section == 'Awards':
                build_section(cv, data, 'Awards', format_awards)

            elif section == 'Education':
                for entry in data[section]:
                    cv.append(NewEntry([
                        entry['Date'], entry['Degree'], entry['Institute'], '']))

    # Add a signature at the bottom
    cv.append(includegraphics(options='width=5cm', arguments='images/Signaturetransparant.png'))


doc.generate_pdf()
doc.generate_tex()