# https://stackoverflow.com/questions/2792650/import-error-no-module-name-urllib2
# inspired by https://limpet.net/mbrubeck/2014/08/11/toy-layout-engine-2.html
from urllib.request import urlopen
import ssl
import sys

class TextNode:

	def __init__(self, text):

		self.text = text

class TagAttribute:

	def __init__(self, name, value=None):

		self.name = name
		self.value = value

class TagNode:

	def __init__(self, name, attributes, children):

		self.name = name
		self.attributes = attributes
		self.children = children

class ParsingException(Exception):

	pass

class Parser:

	def __init__(self, html):

		self.pos = 0
		self.html = html

	def skip_spaces(self):

		while self.current_char().isspace():

			self.pos += 1

	def current_char(self):

		return '' if self.eof() else self.html[self.pos]	

	def expect(self, char):

		if char == self.current_char():

			self.pos += 1
			return

		raise ParsingException('Expected ' + char + ', got ' + self.current_char() + '.')

	def eof(self):

		return self.pos > len(self.html)

	def parse_tag_name(self):

		name = ''
		self.skip_spaces()

		while not self.eof() and \
		  (self.current_char() == '_' or \
		   self.current_char().isalnum()):

			name += self.current_char()
			self.pos += 1

		return name

	def parse_tag_attributes(self):

		attributes = []

		while not self.eof() and self.current_char() != '>':

			name = self.parse_tag_name()
			self.skip_spaces()

			if self.current_char() == '=':

				self.pos += 1
				self.skip_spaces()
				opening_char = self.current_char()
				self.pos += 1
				value = ''

				while not self.eof() and self.current_char() != opening_char:

					if self.current_char() == '\\':

						value += self.current_char()
						self.pos += 1

					value += self.current_char()
					self.pos += 1

				attributes.append(TagAttribute(name, value))
				continue

			attributes.append(TagAttribute(name))

		return attributes

	def parse_tag(self):

		self.expect('<')
		name = self.parse_tag_name()
		attributes = self.parse_tag_attributes()
		self.expect('>')
		children = self.parse()
		self.expect('<')
		closingName = self.parse_tag_name()
		if name != closingName:
			raise ParsingException('Opening tag and closing tag have different names.')
		self.expect('/')
		self.expect('>')

		return TagNode(name, attributes, children)

	def parse_text(self):

		text = ''

		while not self.eof() and self.current_char() != '<':

			text += self.current_char()
			self.pos += 1

		return TextNode(text)

	def parse(self):

		contents = []

		while not self.eof():

			self.skip_spaces()

			if self.current_char() == '<':

				contents.append(self.parse_tag())

			else:

				contents.append(self.parse_text())

			self.skip_spaces()

		return contents

if __name__ == '__main__':

	if len(sys.argv) >= 2:

		my_context = ssl.SSLContext()
		page = urlopen(sys.argv[1], context=my_context)
		parser = Parser(str(page.read()))
		parser.parse()
