import re
from Fighter import Fighter


class FightReport(object):

    def __init__(self):
        # Init attributes.
        self.text_raw = ''
        self.text_teams = []
        self.text_rounds = []
        self.teams = []

    def analyse(self):
        self.consolidate_text()
        self.get_char_info()

    def get_new_report_text(self, path):
        # Read text from file.
        with open(path, encoding='utf-8') as in_file:
            self.text_raw = in_file.read()

    def consolidate_text(self):
        # Get text of teams.
        begin_teams = self.text_raw.find('Verteidiger')
        end_teams = self.text_raw.find('Kampfereignisse (Log)')
        self.text_teams = self.text_raw[begin_teams:end_teams - 3].split('\n')

        # Get text of each round.
        begin_rounds = self.text_raw.find('Kampfereignisse (Log)')
        end_rounds = self.text_raw.find('Hilfe & Informationen')
        text_rounds_raw = self.text_raw[begin_rounds + 22:end_rounds]

        last_index = None
        for index in re.finditer('Runde', text_rounds_raw):
            # Check if it is the first loop.
            if last_index is None:
                last_index = index
                continue
            else:
                text_round_cur = text_rounds_raw[last_index.start() + 8: index.start() - 2]
                self.text_rounds.append(text_round_cur.split('\n'))
                last_index = index

    def get_char_info(self):
        for line in self.text_teams:
            if line.startswith('Verteidiger'):
                cur_team = 0
            elif line.startswith('Angreifer'):
                cur_team = 1
            elif line.startswith('[?]'):
                line_split = line.replace('[?] ', '').split('\t')
                new_fighter = Fighter(line_split[0])
                if line_split[1] == 'kampfunfähig':
                    new_fighter.set_end_values('kampfunfähig', int(line_split[2][:-1]) / 100)
                else:
                    new_fighter.set_end_values('aktiv', int(line_split[2][:-1]) / 100)

                breakpoint()
        pass
