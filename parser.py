"""
  class Parser
  
  This class represents our parser.
"""
class Parser:

    """
      Parser.__init__(self, content)
      
      This function is called whenever a new instance of the Parser class is created.
      
      @param self This instance of the Parser class.
      @param content The text content (grabbed from a website using urllib).
    """
    def __init__(self, content):
        self.content = content
        self.pos = 0

    """
      Parser.discard_while(self, test)
      
      This function skips past characters in our content string
      while the test function is true.
      
      @param self This instance of the Parser class.
      @param test The test function (will return True or False when provided with the current character).
    """
    def discard_while(self, test):
        while self.pos < len(self.content) and test(self.content[self.pos]):
            self.pos += 1

    """
      Parser.discard_spaces(self)
      
      This function skips characters until the current character is not a space (or newline or tab).
      
      @param self This instance of the Parser class.
    """
    def discard_spaces(self):
        self.discard_while(lambda c: c.isspace())

    """
      Parser.record_while(self)
      
      This function append characters in our content string to a new string
      while the test function is true.
      
      @param self This instance of the Parser class.
      @param test The test function (will return True or False when provided with the current character).
      @return The new string.
    """
    def record_while(self, test):
        recorded_string = ''
        while self.pos < len(self.content) and test(self.content[self.pos]):
            recorded_string += self.content[self.pos]
            self.pos += 1

        return recorded_string

    """
      Parser.cleanup(self, string)
      
      This function removes extraneous spaces from a string.
      
      @param self This instance of the Parser class.
      @param string The string to clean up.
      @return The cleaned up string.
    """
    def cleanup(self, string):
        cleaned_up_string = ''
        parts = list(string)
        i = 0
        while i < len(parts):
            if parts[i] == '\\' and i+1 < len(parts) and parts[i+1] in 'nrt':
                i += 2
                continue

            cleaned_up_string += parts[i]
            i += 1

        return cleaned_up_string.strip()

    """
      Parser.parse(self)
      
      This function will parse the html string, and will return text elements (considered relevent for now).
      
      @param self This instance of the Parser class.
      @return A list of recorded strings from text elements.
    """
    def parse(self):
        recorded_strings = []
        discard_next_string = False
        while self.pos < len(self.content):
            if self.content[self.pos] == '<':
                self.pos += 1
                self.discard_spaces()

                if ((self.pos + 6 <= len(self.content) and self.content[self.pos:self.pos+6] == 'script') or \
                    (self.pos + 5 <= len(self.content) and self.content[self.pos:self.pos+5] == 'style')):
                    discard_next_string = True

                self.discard_while(lambda c: c != '>')
                self.pos += 1
            else:
                if discard_next_string:
                    self.discard_while(lambda c: c != '<')
                    discard_next_string = False
                else:
                    string = self.record_while(lambda c: c != '<').strip()
                    cleaned_up_string = self.cleanup(string)
                    if len(cleaned_up_string) > 0:
                        recorded_strings.append(cleaned_up_string)

        return recorded_strings
