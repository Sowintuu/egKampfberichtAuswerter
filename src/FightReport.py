import re


class FightReport(object):
    PATTERN_BEGIN = re.compile('Alle Kampfrunden anzeigen')

    def __init__(self):
        # Init attributes.
        self.text_teams = ''
        self.text_rounds = ''
        self.teams = []

    def analise(self):
        # Get the player names and final status.
        self.get_char_info()


    def get_new_report_text(self, path):
        # Read text from file.
        with open(path) as in_file:
            text = in_file.read()

        # Get text of teams.
        begin_teams = text.find('Verteidiger')
        end_teams = text.find('Kampfereignisse (Log)')
        self.text_teams = text[begin_teams:end_teams]

        # Get text of each round.
        begin_rounds = text.find('Kampfereignisse (Log)')
        end_rounds = text.find('Hilfe & Informationen')
        text_rounds = text[begin_rounds+22:end_rounds]
        round_begins = re.findall('Runde', text_rounds)

        breakpoint()

    def get_char_info(self):
        pass