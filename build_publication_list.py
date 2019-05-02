__author__ = 'nicholas'

import yaml

from cv_preamble import *
from datetime import datetime

# Get data for cv.
with  open('research_experiences.yaml') as f:
    data= yaml.load(f, Loader=yaml.FullLoader)

# Create Latex file, and the CV object to build sections out of.
doc = get_cv_doc('docs/delgrosso_publications')
with doc.create(CV(data, arguments='List of Publications')) as cv:

    cv.build_section('Journal Publications', lambda x: Description(x))

doc.generate_pdf()
doc.generate_tex()
