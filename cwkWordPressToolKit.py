import sublime, sublime_plugin
import os, sys, codecs, re

VERSION = "0.1b"

#
#  CWK WordPress ToolKit
#

class CwkWordPressParser(sublime_plugin.TextCommand,):

	def __init__(self, *args, **kwargs):
		sublime_plugin.TextCommand.__init__(self, *args, **kwargs)

	def run(self, edit, opening_tag="", closing_tag="", sub_opening_tag="", sub_closing_tag="", attr="", sub_attr="", use_header=False, use_sub_header=False, sub_header_delimiter="|", newline=True):

		self.opening_tag = opening_tag
		self.closing_tag = closing_tag
		self.sub_opening_tag = sub_opening_tag
		self.sub_closing_tag = sub_closing_tag
		self.attr = attr
		self.sub_attr = sub_attr
		self.use_header = use_header
		self.use_sub_header = use_sub_header
		self.sub_header_delimiter = '\\' + sub_header_delimiter
		self.newline = newline


		if self.opening_tag:
			# get active window and view
			window = sublime.active_window()
			view = window.active_view()

			for region in view.sel():
				if not region.empty():
					currentSelection = view.substr(region)  

					if self.attr:
						tag_delimiter = self.opening_tag[-1]
						if self.use_header == 'True':
							self.opening_tag = opening_tag[:-1] + " " + self.attr + "=" + '"' + currentSelection.splitlines()[0]  + '"' + tag_delimiter
							currentSelection = currentSelection.splitlines()[1:]
						else:
							self.opening_tag = opening_tag[:-1] + " " + self.attr + tag_delimiter
							currentSelection = currentSelection.splitlines()
					else:
						currentSelection = currentSelection.splitlines()
					if self.sub_opening_tag:
						if self.sub_attr:
							tag_delimiter = sub_opening_tag[-1]
							self.sub_opening_tag = sub_opening_tag[:-1] + " " +  self.sub_attr + tag_delimiter						
						lines = []
						for line in currentSelection:
							if self.use_sub_header == 'True':
								sub_lines = re.split(self.sub_header_delimiter, line)
								if sub_lines:
									sub_header = sub_lines[0].strip()
									line = "".join(sub_lines[1:]).strip()
								else:
									sub_header = "Header Placeholder"

								self.sub_opening_tag = sub_opening_tag[:-1] + " " + self.sub_attr + "=" + '"' + sub_header + '"' + tag_delimiter
								currentSelection = currentSelection[1:]


							lines.append( self.sub_opening_tag + line + self.sub_closing_tag )
						if self.newline != 'False':
							currentSelection =  self.opening_tag + "\n" + "\n".join( lines )  + "\n" +  self.closing_tag
						else:
							currentSelection =  self.opening_tag + "".join( lines )  +  self.closing_tag

					else: 
						if self.newline != 'False':
							currentSelection = self.opening_tag + "\n" +  "\n".join( currentSelection ) + "\n" +  self.closing_tag
						else:
							currentSelection = self.opening_tag + "".join( currentSelection )  +  self.closing_tag

					view.replace(edit, region, currentSelection)

