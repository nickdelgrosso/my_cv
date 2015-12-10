__author__ = 'nicholas'

import yaml
from pylatex import Document, Section, Subsection, Command, Package, UnsafeCommand, Itemize
from pylatex.base_classes import CommandBase, Arguments
from pylatex.utils import italic, NoEscape, bold
from pylatex.document import Environment
from collections import defaultdict

doc = Document('docs/delgrosso_cv',
               documentclass='article')

# Set Packages
doc.packages.append(Package('marginnote'))
doc.packages.append(UnsafeCommand('reversemarginpar'))
doc.packages.append(Package('graphicx'))
doc.packages.append(Package('classicthesis', options='nochapters'))
doc.packages.append(Package('currvita', options='LabelsAligned'))
doc.packages.append(Package('hyperref'))
doc.packages.append(UnsafeCommand('hypersetup', extra_arguments=r'colorlinks, breaklinks, urlcolor=Maroon, linkcolor=Maroon'))

doc.packages.append(UnsafeCommand('newlength', r'\datebox', ))
doc.packages.append(UnsafeCommand('settowidth', r'\datebox', extra_arguments='Tuebingen, Germany'))

doc.packages.append(UnsafeCommand('renewcommand', r'\cvheadingfont', extra_arguments=r'\LARGE\color{Maroon}'))


# Make New Commands via a metaclass
for name in ['MarginText', 'NewEntry', 'Description', 'DescMarg', 'SubHeading', 'EntryHeader',
             'vspace', 'hspace', 'includegraphics', 'Email']:
    globals()[name] = type(name, (CommandBase,), {'_latex_name': name})

# Custom CV Environment behavior
class CV(Environment):
    _latex_name = 'cv'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arguments = UnsafeCommand('spacedallcaps', self.arguments)


# Unchanged-ish (Extra line break at the end)
doc.packages.append(UnsafeCommand('newcommand', r'\SubHeading', options=1,
                         extra_arguments=r'\vspace{.5em}\noindent\spacedlowsmallcaps{#1}\vspace{0.7em}\\'))

doc.packages.append(UnsafeCommand('newcommand', r'\Email', options=1,
                         extra_arguments=r'\href{mailto:#1}{#1}'))

# Unchanged
doc.packages.append(UnsafeCommand('newcommand', r'\MarginText', options=1, extra_arguments=r'\marginpar{\raggedleft\small#1}'))

# Unchanged
doc.packages.append(UnsafeCommand('newcommand', r'\Description', options=1,
                         extra_arguments=r'\hangindent=2em\hangafter=0\footnotesize{#1}\par\normalsize\vspace{1em}'))

doc.packages.append(UnsafeCommand('newcommand', r'\DescMarg', options=2,
                         extra_arguments=r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small} \MarginText{#1} #2 \vspace{0.5em}\\'))

##################
doc.packages.append(UnsafeCommand('newcommand', r'\EntryHeader', options=3,
                         extra_arguments=r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small \textit{#2}}\hspace{1.5em} \MarginText{#1} #3 \vspace{0.5em}'))

doc.packages.append(UnsafeCommand('newcommand', r'\NewEntry', options=4,
        extra_arguments=r'\EntryHeader{#1}{#2}{#3}\\\Description{#4}'))




# Fill Document
doc.append(UnsafeCommand('thispagestyle', 'empty'))
doc.append(NoEscape(r'\raggedright'))

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