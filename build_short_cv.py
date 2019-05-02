__author__ = 'nicholas'

import yaml

from cv_preamble import *
from datetime import datetime

# Get data for cv.
with  open('research_experiences.yaml') as f:
    data= yaml.load(f, Loader=yaml.FullLoader)

# Create Latex file, and the CV object to build sections out of.
doc = get_cv_doc('docs/delgrosso_short_cv')
with doc.create(CV(data, arguments='Curriculum Vitae')) as cv:

    def format_personal(entry):
        for key, value in entry.items():
            if 'mail' in key:
                value = Email(value)
            return HeaderOnly([key, value])

    cv.build_section('Education', lambda x: NewEntry([x['Date'], x['Degree'], x['Institute'], '']))

    cv.build_section('Research Experience', lambda x: NewEntry([' -\n  '.join([x['StartDate'], x['EndDate']]),
                                                                       x['Institute'], x['Supervisor'], x['Description']]))

doc.generate_pdf()
doc.generate_tex();
