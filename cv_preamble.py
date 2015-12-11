from collections import defaultdict
from pylatex import Document, Section, Subsection, Command, Package, UnsafeCommand, Itemize
from pylatex.base_classes import CommandBase, Arguments
from pylatex.utils import italic, NoEscape, bold
from pylatex.document import Environment

from dateutil import parser as dateparser
from datetime import datetime
import warnings

def get_cv_doc(filename):
    """Returns a pylatex.Document instance pre-loaded with everything needed for my cv style."""
    doc = Document(filename,
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

    # Unchanged-ish (Extra line break at the end)
    doc.packages.append(UnsafeCommand('newcommand', r'\SubHeading', options=1,
                             extra_arguments=r'\vspace{1em}\noindent\spacedlowsmallcaps{#1}\vspace{0.7em}\\'))

    doc.packages.append(UnsafeCommand('newcommand', r'\Email', options=1,
                             extra_arguments=r'\href{mailto:#1}{#1}'))

    # Unchanged
    doc.packages.append(UnsafeCommand('newcommand', r'\MarginText', options=1, extra_arguments=r'\marginpar{\raggedleft\small#1}'))

    # Unchanged
    doc.packages.append(UnsafeCommand('newcommand', r'\Description', options=1,
                             extra_arguments=r'\hangindent=2em\hangafter=0\footnotesize{#1}\par\normalsize\vspace{1em}'))

    doc.packages.append(UnsafeCommand('newcommand', r'\DescMarg', options=2,
                             extra_arguments=r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small} \MarginText{#1} #2 \vspace{0.3em}\\'))

    ##################
    doc.packages.append(UnsafeCommand('newcommand', r'\HeaderOnly', options=2,
                                      extra_arguments= r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small \textit{#1}}\hspace{1.5em} #2 \vspace{0.5em}\\'))

    doc.packages.append(UnsafeCommand('newcommand', r'\EntryHeader', options=3,
                             extra_arguments=r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small \textit{#2}}\hspace{1.5em} \MarginText{#1} #3 \vspace{0.5em}'))

    doc.packages.append(UnsafeCommand('newcommand', r'\NewEntry', options=4,
            extra_arguments=r'\EntryHeader{#1}{#2}{#3}\\\Description{#4}'))




    # Fill Document
    doc.append(UnsafeCommand('thispagestyle', 'empty'))
    doc.append(NoEscape(r'\raggedright'))

    return doc

# Make New Commands via a metaclass
for name in ['MarginText', 'NewEntry', 'Description', 'DescMarg', 'SubHeading', 'EntryHeader', 'HeaderOnly',
             'vspace', 'hspace', 'includegraphics', 'Email']:
    globals()[name] = type(name, (CommandBase,), {'_latex_name': name})

# Custom CV Environment behavior
class CV(Environment):
    _latex_name = 'cv'
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cvdata = data
        self.arguments = UnsafeCommand('spacedallcaps', self.arguments)
        self.append(vspace('2em')) # Space between title and the first section

    def build_section_itemized(self, section_name, item_formatter):
        self.append(SubHeading(section_name))
        for entry in self.cvdata[section_name]:
            with self.create(Itemize()) as itemize:
                itemize.add_item(item_formatter(entry))

    def build_section(self, section_name, formatter, datefilter=None, datefield=''):
        self.append(SubHeading(section_name))
        for entry in self.cvdata[section_name]:
            if isinstance(entry, dict):
                entry = defaultdict(str, entry)
                if datefilter:
                    assert isinstance(datefilter, datetime), "datefilter must be a datetime or timedelta object"
                    if datefield in entry:
                        try:
                            entry_date = dateparser.parse(entry[datefield])
                        except ValueError:
                            if isinstance(entry[datefield], str) and entry[datefield].lower() in ['today', 'present', 'now', 'current']:
                                entry_date = datetime.now()
                            else:
                                print('Warning: Could not dateparse entry date: {}.  This entry will be automatically rejected.'.format(entry[datefield]))
                            continue
                        # Reject dates before the datefilter date.
                        if isinstance(datefilter, datetime):
                            if entry_date < datefilter:
                                continue

            self.append(formatter(entry))


def datefilter(entry, field, filter_date):
    """Returns True if filter is passed, False if not."""
    filter_date = dateparse_str(filter_date) if isinstance(filter_date, str) else filter_date
    assert isinstance(filter_date, datetime), "filter_date not recognized as a date."
    try:
        entry_date = dateparse_str(entry[field])
        return entry_date > filter_date
    except ValueError:
        warnings.warn('entry_date, "{}", not recognized.  Rejecting this entry.'.format(entry_date))
        return False


def dateparse_str(value):
    """Returns a datetime object from a string, using a modified version of the dateutil parser"""
    if entry[datefield].lower() in ['today', 'present', 'now', 'current']:
        return datetime.now()
    else:
        return dateparser.parse(value)


