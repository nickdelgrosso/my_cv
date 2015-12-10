from pylatex import Document, Section, Subsection, Command, Package, UnsafeCommand, Itemize
from pylatex.base_classes import CommandBase, Arguments
from pylatex.utils import italic, NoEscape, bold
from pylatex.document import Environment

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arguments = UnsafeCommand('spacedallcaps', self.arguments)