__author__ = 'nicholas'

from pylatex import Document, Section, Subsection, Command, Package, UnsafeCommand
from pylatex.base_classes import CommandBase, Arguments
from pylatex.utils import italic, NoEscape
from pylatex.document import Environment


doc = Document('docs/delgrosso_cv',
               documentclass='article')

# Set Packages
doc.packages.append(Package('marginnote'))
doc.packages.append(Package('graphicx'))
doc.packages.append(Package('classicthesis', ['nochapters']))
doc.packages.append(Package('currvita', ['LabelsAligned']))
doc.packages.append(Package('hyperref'))
#
# Make New Commands
class CV(Environment):
    _latex_name = 'cv'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arguments = UnsafeCommand('spacedallcaps', self.arguments)

class MarginText(CommandBase):
    _latex_name = 'MarginText'
doc.append(UnsafeCommand('newcommand', r'\MarginText', options=1,
                 extra_arguments=r'\marginpar{\raggedleft\small#1}')
           )

doc.append(UnsafeCommand('newlength', r'\datebox', ))
doc.append(UnsafeCommand('settowidth', r'\datebox', extra_arguments='Tuebingen, Germany'))


##
class NewEntry(CommandBase):
    _latex_name = 'NewEntry'
doc.append(UnsafeCommand('newcommand', r'\NewEntry', options=2,
              extra_arguments=r'\noindent\hangindent=2em\hangafter=0 \parbox{\datebox}{\small \textit{#1}}\hspace{1.5em} #2 \vspace{0.5em}\\')
           )

##
doc.append(UnsafeCommand('hypersetup',
                         extra_arguments=r'colorlinks, breaklinks, urlcolor=Maroon, linkcolor=Maroon')
           )

doc.append(UnsafeCommand('renewcommand', r'\cvheadingfont', extra_arguments=r'\LARGE\color{Maroon}')
           )

##
class Description(CommandBase):
    _latex_name = 'Description'
doc.append(UnsafeCommand('newcommand', r'\Description', options=1,
                         extra_arguments=r'\hangindent=2em\hangafter=0\noindent\raggedright\footnotesize{#1}\par\normalsize\vspace{1em}')
           )

##
class SubHeading(CommandBase):
    _latex_name = 'SubHeading'
doc.append(UnsafeCommand('newcommand', r'\SubHeading', options=1,
                         extra_arguments=r'\vspace{.5em}\noindent\spacedlowsmallcaps{#1}\vspace{0.7em}\\'))

class VSpace(CommandBase):
    _latex_name = 'vspace'

class HSpace(CommandBase):
    _latex_name = 'hspace'

class IncludeGraphics(CommandBase):
    _latex_name = 'includegraphics'

# Fill Document
with doc.create(CV(arguments='Nicholas A. Del Grosso')) as cv:

    cv.append(UnsafeCommand('vspace', '2em'))
    cv.append(SubHeading('Research Experiences'))
    cv.append(NewEntry(['Universitat Tuebingen', 'Prof. Dr. Niels Birbaumer']))
    cv.append(MarginText('May 2013'))
    cv.append(Description('This is a description of what I did during this time.  It is the longest part of the entry, and can take up several lines.  Hopefully, it will look really good.'))

    cv.append(VSpace('2em'))
    cv.append(IncludeGraphics(options='width=5cm', arguments='images/Signaturetransparant.png'))

doc.generate_pdf()
doc.generate_tex()