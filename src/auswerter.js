
function auswerten() {
    let t_input = document.getElementById('input');
    let text = t_input.value;

    text = consolidate_text(text)

    let fighters = get_char_info(text[0])

    if (fighters == null) {
        return;
    }

    let results = analyse_main_report(text[1], fighters)


    alert('foo')
}
// Extract the teams info from the end of fight and fight rounds.
function consolidate_text(text) {
    // Get text of teams.
    let text_teams = text.substring(
        text.indexOf('Verteidiger'),
        text.indexOf('Kampfereignisse (Log)')
    );

    // Get text of rounds.
    let text_rounds = text.substring(
        text.indexOf('Kampfereignisse (Log)\nRunde ') + 28,
        text.indexOf('Hilfe & Informationen')
    );
    let rounds_split = text_rounds.split('Runde');

    // Combine and return.
    return [text_teams, rounds_split];

}

// Get info from the end of the fight.
function get_char_info(text) {
    // Init some vars.
    let cur_team = null;
    let fighters = {};
    let line;

    // Split text by lines.
    let lines = text.split('\n');

    // Loop over lines to get fighters and their information.
    for (let i = 0; i < lines.length; i++) {
        line = lines[i];

        // Determine the team of the fighter.
        if (line.startsWith('Verteidiger')) {
            cur_team = 0;
        } else if (line.startsWith('Angreifer')) {
            cur_team = 1;

        // Collect data from the line.
        } else if (line.startsWith('[?]')) {
            if (cur_team == null) {
                alert('Fehler: Unvollständiger Kampfbericht vermutet');
                return null;
            }

            let line_split = line.replace('[?] ', '').split('\t')
            fighters[line_split[0]] = {
                name: line_split[0],
                team: cur_team,
                status: line_split[1],
                health_rel_end: parseFloat(line_split[2].substring(0, line_split[2].length-1)) / 100,
                dmg_done: 0,
                dmg_received: 0,
                heal_done: 0,
                heal_received: 0,
                actions: {},
            };
        }
    }

    return fighters;
}

function analyse_main_report(rounds, fighters) {
    // Init variables.
    let fighter_names = Object.keys(fighters);
    let time;
    let main;
    let main_reduced;
    let result;
    let actor;
    let aim;
    let tool_match;
    let tool;
    let action;


    // Init regex patterns.
    let pattern_tool = new RegExp('(?<=\\[).+(?=\\])')
    let pattern_space2p = new RegExp(' {2,}')
    let pattern_damage = new RegExp('\d+ Schaden')

    // Loop over rounds.
    for (let r = 0; r < rounds.length; r++) {
        // Split round into lines.
        let lines = rounds[r].split('\n');

        // Loop over lines.
        for (let l = 1; l < lines.length; l++) {
            // Get parts: time, main and result, if present.
            time = lines[l].substring(0, lines[l].indexOf(' '))
            main = lines[l].substring(lines[l].indexOf(' ')+1, lines[l].lastIndexOf(':'));
            result = lines[l].substring(lines[l].lastIndexOf(':')+2, lines[l].lastIndexOf('.'))

            // Get fighter names.
            actor = null;
            aim = null;

            // If the line starts with '[', there is no actor.
            if (main.startsWith('[')) {
                actor = 'none'
            }

            // Loop over fighter names to find out actor and aim.
            for (let fi = 0; fi < fighter_names.length; fi++) {
                // Check if the current fighter is the actor.
                if (main.startsWith(fighter_names[fi])) {
                    actor = fighters[fighter_names[fi]];
                    // Check if actor == aim.
                    if (main.substring(actor.name.length, main.length).includes(actor.name)) {
                        aim = fighters[fighter_names[fi]];
                    }
                } else if (main.includes(fighter_names[fi])) {
                    aim = fighters[fighter_names[fi]];
                }
                // Break, if actor and aim assigned.
                if (actor != null && aim != null) {
                    break;
                }
            }

            // Check for tool.
            tool_match = pattern_tool.exec(main);
            if (tool_match != null) {
                tool = tool_match[0];
            }

            // Remove fighters and tool names to get action.
            if (actor != null) {
                main_reduced = main.replace(actor.name, '');
            }
            if (aim != null) {
                main_reduced = main_reduced.replace(aim.name, '');
            }
            if (tool != null) {
                main_reduced = main_reduced.replace('[' + tool + ']', '');
            }
            action = main_reduced.trim();
            action = action.replace(pattern_space2p, ' ');

            // Process result and action.



            dmg_match = pattern_damage.exec(result);
            if (dmg_match != null) {

            }
            let x;

        }

    }

    let x;


}


let b_submit  = document.getElementById('submit');
b_submit.addEventListener ('click', auswerten, true);
