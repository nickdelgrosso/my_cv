__author__ = 'nicholas'

import yaml
from cv_preamble import *

doc = get_cv_doc('docs/delgrosso_cv')

with doc.create(CV(arguments='Nicholas A. Del Grosso')) as cv:

    # Space between title and the first section
    cv.append(vspace('2em'))

    with open('research_experiences.yaml') as f:

        data = yaml.load(f)

        def format_personal(entry):
            for key, value in entry.items():
                if 'mail' in key:
                    value = Email(value)
                return HeaderOnly([key, value])
        build_section(cv, data, 'Personal Info', format_personal)

        build_section_itemized(cv, data, 'Goals', lambda x: x)

        build_section(cv, data, 'Education', lambda x: NewEntry([x['Date'], x['Degree'], x['Institute'], '']))

        build_section(cv, data, 'Research Experience', lambda x: NewEntry([' -\n  '.join([x['StartDate'], x['EndDate']]),
                                                                           x['Institute'], x['Supervisor'], x['Description']]))

        build_section(cv, data, 'Industry Experience', lambda x: NewEntry([' -\n '.join(x['StartDate', x['EndDate']]),
                                                                           x['Position'], x['Institute'], x['Description']]))

        build_section(cv, data, 'Journal Publications', lambda x: Description(x))

        build_section(cv, data, 'Conference Publications', lambda x: NewEntry([x['Date'], x['Conference'],
                                                                               x['Title'], x['Description']]))

        def format_skill_item(entry):
            return bold(entry) + NoEscape(': ') + NoEscape(', '.join(entry.values()))
        # build_section_itemized(cv, data, 'Skills', format_skill_item)

        build_section(cv, data, 'Awards', lambda x: DescMarg([x['Date'], x['Title']]))

    # Add a signature at the bottom
    cv.append(includegraphics(options='width=5cm', arguments='images/Signaturetransparant.png'))


doc.generate_pdf()
doc.generate_tex();