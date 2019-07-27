class Parser:

    def __init__(self, content):
        self.content = content
        self.pos = 0

    def discard_while(self, test):
        while self.pos < len(self.content) and test(self.content[self.pos]):
            self.pos += 1

    def discard_spaces(self):
        self.discard_while(lambda c: c.isspace())

    def record_while(self, test):
        recorded_string = ''
        while self.pos < len(self.content) and test(self.content[self.pos]):
            recorded_string += self.content[self.pos]
            self.pos += 1

        return recorded_string

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
