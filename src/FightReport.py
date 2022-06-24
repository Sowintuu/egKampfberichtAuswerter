import re
from Fighter import Fighter


class FightReport(object):

    TOOL_PATTERN = re.compile(r'(?<=\[).+(?=\])')
    SPACE_PATTERN = re.compile(r' {2,}')

    def __init__(self):
        # Init attributes.
        self.text_raw = ''
        self.text_teams = []
        self.text_rounds = []
        self.teams = [[]]
        self.teams.append([])
        self.fighter_name_list = []

        self._cur_line = ''

    def analyse(self):
        # Extract the important parts of the text.
        self.consolidate_text()

        # Get the character information from end report.
        self.get_char_info_end()

        # Get detailed information from main report.
        self.analyse_main_report()

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

    def get_char_info_end(self):
        # Init cur_team.
        cur_team = None

        # Loop over lines to get fighters and their information.
        for line in self.text_teams:
            # Set cur_team to 0 or 1, if it is a header.
            if line.startswith('Verteidiger'):
                cur_team = 0
            elif line.startswith('Angreifer'):
                cur_team = 1
            # Get information, if it starts with [?].
            elif line.startswith('[?]'):
                # Check if a team was determined.
                if cur_team is None:
                    raise Exception('Bad report format suspected.')

                # Split the line to get the information.
                line_split = line.replace('[?] ', '').split('\t')
                new_fighter = Fighter(line_split[0])
                if line_split[1] == 'kampfunfähig':
                    new_fighter.set_end_values('kampfunfähig', int(line_split[2][:-1]) / 100)
                else:
                    new_fighter.set_end_values('aktiv', int(line_split[2][:-1]) / 100)

                # Add the fighter to the respective team and name list.
                self.teams[cur_team].append(new_fighter)
                self.fighter_name_list.append(new_fighter.name)

    def analyse_main_report(self):
        for rnd in self.text_rounds:
            for line in rnd:
                self._cur_line = line
                self.analyse_line()

    def analyse_line(self):
        # Split line at spaces and remove time stamp and trailing dot.
        line_split = self._cur_line.strip('.').split()[1:]

        # Concat line without timestamp
        line = ' '.join(line_split)

        # Get result part, if present. Remove the result part from line
        line_colon_split = line.split(':')
        line = line_colon_split[0]
        if len(line_colon_split) > 1:
            result = line_colon_split[1].strip()
        else:
            result = None

        # Get possible fighter names (actor and aim).
        actor = None
        aim = None
        for fighter in self.fighter_name_list:
            if line.startswith(fighter):
                actor = fighter
                # Check if actor == aim.
                line_no_actor = line[len(actor):]
                if fighter in line_no_actor:
                    aim = fighter
            elif fighter in line:
                aim = fighter
            if actor is not None and aim is not None:
                break

        # Get tool name.
        tool = None
        tool_match = self.TOOL_PATTERN.search(line)
        if tool_match is not None:
            tool = tool_match.group(0)

        # Remove fighters and tool names to get action.
        line_reduced = line
        if actor is not None:
            line_reduced = line.replace(actor, '')
        if aim is not None:
            line_reduced = line_reduced.replace(aim, '')
        if tool is not None:
            line_reduced = line_reduced.replace('[' + tool + ']', '')
        action = line_reduced.strip('.').strip(' ')
        action = self.SPACE_PATTERN.sub(' ', action)

        #

        breakpoint()

    # Get a fighter from the fighter list by its name.
    def get_fighter_by_name(self, name):
        for team in self.teams:
            for fighter in team:
                if fighter.name == name:
                    return fighter
