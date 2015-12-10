__author__ = 'nicholas'

import yaml
from collections import defaultdict
from cv_preamble import *

doc = get_cv_doc('docs/delgrosso_cv')

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
                for entry in data[section]:
                    entry = defaultdict(str, entry)
                    cv.append(NewEntry([
                        ' -\n  '.join([entry['StartDate'], entry['EndDate']]),
                        entry['Institute'],
                        entry['Supervisor'],
                        entry['Description']
                    ]))

            elif section == 'Industry Experience':
                for entry in data[section]:
                    entry = defaultdict(str, entry)
                    cv.append(NewEntry([
                        ' -\n '.join(entry['StartDate', entry['EndDate']]),
                        entry['Position'],
                        entry['Institute'],
                        entry['Description']
                    ]))

            elif section == 'Journal Publications':
                for entry in data[section]:
                    cv.append(Description(entry))

            elif section == 'Conference Publications':
                for entry in data[section]:
                    entry = defaultdict(str, entry)
                    cv.append(NewEntry([
                        entry['Date'],
                        entry['Conference'],
                        entry['Title'],
                        entry['Description']
                    ]))

            elif section == 'Skills':
                with doc.create(Itemize()) as itemize:
                    for entry in data[section]:
                        itemize.add_item(bold(entry) + NoEscape(': ') + NoEscape(', '.join(data[section][entry])))

            elif section == 'Goals':
                for entry in data[section]:
                    with doc.create(Itemize()) as itemize:
                        itemize.add_item(entry)

            elif section == 'Awards':
                for entry in data[section]:
                    cv.append(DescMarg([entry['Date'], entry['Title']]))

            elif section == 'Education':
                for entry in data[section]:
                    cv.append(NewEntry([
                        entry['Date'], entry['Degree'], entry['Institute'], '']))

            # Spacing between sections
            cv.append(vspace('2em'))

    # Add a signature at the bottom
    cv.append(includegraphics(options='width=5cm', arguments='images/Signaturetransparant.png'))


doc.generate_pdf()
doc.generate_tex()