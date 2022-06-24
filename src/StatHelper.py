import os
import re
from datetime import datetime
from tkinter import Tk, Text, Button, Entry, Label
from tkinter import filedialog as fd

PAT_SPLIT_BLOCK = re.compile(r'\s{2,}')
PAT_SPLIT_PARTS = re.compile(r'Attribute \[\?\]\n|Werte im Nahkampf\n|Werte im Fernkampf\n|\n\nWerte beim Bandagieren')
PAT_LP_MAX = re.compile(r'LP\: \d+ \/ \d+')
PAT_STR = re.compile(r'(?<=Stärke)\s+\d+')
PAT_DEX = re.compile(r'(?<=Geschicklichkeit)\s+\d+')
PAT_KON = re.compile(r'(?<=Konstitution)\s+\d+')
PAT_INT = re.compile(r'(?<=Intelligenz)\s+\d+')


def stat_helper():
    loop('manual')


def loop(mode):
    results = []
    export_done = False

    while True:
        text_res, do_finish = input_window()

        # # ###### DEBUG ###### #
        # with open(r'..\temp\stat_input.txt', encoding="utf-8") as i_file:
        #     text_res = i_file.read()
        #     do_finish = True
        # # ###### DEBUG ###### #

        if text_res.strip() != '':
            parse_stat_input(text_res, results)

        if do_finish:
            # Export results.
            if len(results) > 0:
                export_done = export_results(results)

        if export_done:
            break


# create an input window.
def input_window(*title_text, attrib_in=(5, 5, 5, 5)):
    # Init attrib.
    finish = [False]

    # Create master window.
    master = Tk()
    master.title(title_text)

    # # Create attribute entries.
    # n_col = 0
    # Label(text='Stärke', justify='center').grid(row=0, column=n_col)
    # b_str_p = Button(master, text='^', width=4, command=lambda: pm_bc('+', 'str'))
    # b_str_p.grid(row=1, column=n_col)
    # e_str = Entry(master, justify='center', width=5)
    # e_str.delete(0, 'end')
    # e_str.insert(0, attrib[0])
    # e_str.grid(row=2, column=n_col)
    # b_str_m = Button(master, text='v', width=4, command=lambda: pm_bc('-', 'str'))
    # b_str_m.grid(row=3, column=n_col)
    #
    # n_col += 1
    # Label(text='Geschicklichkeit', justify='center').grid(row=0, column=n_col)
    # b_dex_p = Button(master, text='^', width=4, command=lambda: pm_bc('+', 'dex'))
    # b_dex_p.grid(row=1, column=n_col)
    # e_dex = Entry(master, justify='center', width=5)
    # e_dex.delete(0, 'end')
    # e_dex.insert(0, attrib[1])
    # e_dex.grid(row=2, column=n_col)
    # b_dex_m = Button(master, text='v', width=4, command=lambda: pm_bc('-', 'dex'))
    # b_dex_m.grid(row=3, column=n_col)
    #
    # n_col += 1
    # Label(text='Konstitution', justify='center').grid(row=0, column=n_col)
    # b_kon_p = Button(master, text='^', width=4, command=lambda: pm_bc('+', 'kon'))
    # b_kon_p.grid(row=1, column=n_col)
    # e_kon = Entry(master, justify='center', width=5)
    # e_kon.delete(0, 'end')
    # e_kon.insert(0, attrib[2])
    # e_kon.grid(row=2, column=n_col)
    # b_kon_m = Button(master, text='v', width=4, command=lambda: pm_bc('-', 'kon'))
    # b_kon_m.grid(row=3, column=n_col)
    #
    # n_col += 1
    # Label(text='Intelligenz', justify='center').grid(row=0, column=n_col)
    # b_int_p = Button(master, text='^', width=4, command=lambda: pm_bc('+', 'int'))
    # b_int_p.grid(row=1, column=n_col)
    # e_int = Entry(master, justify='center', width=5)
    # e_int.delete(0, 'end')
    # e_int.insert(0, attrib[3])
    # e_int.grid(row=2, column=n_col)
    # b_int_m = Button(master, text='v', width=4, command=lambda: pm_bc('-', 'int'))
    # b_int_m.grid(row=3, column=n_col)

    t = Text(master)
    t.grid(row=4, column=0, columnspan=4)
    t.focus_set()

    text_get = []

    # Define callback for finish.
    def next_cb():
        text_get.append(t.get("1.0", 'end'))
        master.destroy()
        finish[0] = False

    def finish_cb():
        text_get.append(t.get("1.0", 'end'))
        master.destroy()
        finish[0] = True

    # Define callback for buttons.
    # def pm_bc(pm, attrib_cb):
    #     if attrib_cb == 'str':
    #         attrib[0] += int(pm + '1')
    #         if attrib[0] < 0:
    #             attrib[0] = 0
    #         e_str.delete(0, 'end')
    #         e_str.insert(0, attrib[0])
    #     elif attrib_cb == 'dex':
    #         attrib[1] += int(pm + '1')
    #         if attrib[1] < 0:
    #             attrib[1] = 0
    #         e_dex.delete(0, 'end')
    #         e_dex.insert(0, attrib[1])
    #     elif attrib_cb == 'kon':
    #         attrib[2] += int(pm + '1')
    #         if attrib[2] < 0:
    #             attrib[2] = 0
    #         e_kon.delete(0, 'end')
    #         e_kon.insert(0, attrib[2])
    #     elif attrib_cb == 'int':
    #         attrib[3] += int(pm + '1')
    #         if attrib[3] < 0:
    #             attrib[3] = 0
    #         e_int.delete(0, 'end')
    #         e_int.insert(0, attrib[3])

    b_next = Button(master, text="Weiter", width=10, command=next_cb)
    b_next.grid(row=5, column=0, columnspan=2)

    b_finish = Button(master, text="Beenden", width=10, command=finish_cb)
    b_finish.grid(row=5, column=2, columnspan=2)

    master.mainloop()

    return text_get[0], finish[0]


def parse_stat_input(text_parse, results):
    # Remove footer.
    text_parse = text_parse.split('Hilfe & Informationen')[0].strip()

    # Split text into parts.
    parts = PAT_SPLIT_PARTS.split(text_parse)

    # Get attributes.
    results_temp = {'Stärke': {'value': int(PAT_STR.search(parts[1]).group(0)), 'unit': ''},
                    'Geschicklichkeit': {'value': int(PAT_DEX.search(parts[1]).group(0)), 'unit': ''},
                    'Konstitution': {'value': int(PAT_KON.search(parts[1]).group(0)), 'unit': ''},
                    'Intelligenz': {'value': int(PAT_INT.search(parts[1]).group(0)), 'unit': ''}}

    # Get max. LP.
    max_lp_text = PAT_LP_MAX.search(parts[0])
    if max_lp_text is not None:
        max_lp_text = max_lp_text.group(0)
        max_lp = int(max_lp_text.split(' / ')[1])
    else:
        max_lp = None

    results_temp['Maximale LP'] = {'value': max_lp, 'unit': ''}

    # Loop over parts.
    for part_id, part in enumerate(parts[2:4]):
        # Get part name.
        if part_id:
            part_name = 'FK'
        else:
            part_name = 'NK'

        # Split text into blocs.
        blocs = PAT_SPLIT_BLOCK.split(part)

        # Loop over first half of the blocs.
        for bloc_id, bloc in enumerate(blocs):
            # Stop, if first half is done.
            if bloc_id >= len(blocs) / 2:
                break

            # Get result bloc.
            bloc_res_id = round(bloc_id + len(blocs) / 2)
            bloc_res = blocs[bloc_res_id]

            # Split in lines and loop starting from the second line.
            bloc_lines = bloc.split('\n')
            bloc_res_lines = bloc_res.split('\n')

            # Insert dummy at first line.
            bloc_res_lines.insert(0, '')

            # Init bloc title.
            bloc_title = ''

            # Loop over lines to get results
            for line_id, line in enumerate(bloc_lines):
                # First line is bloc_title.
                if line_id == 0:
                    bloc_title = line
                    continue

                # Get result name
                res_name = f'{part_name} - {bloc_title} - {line}'

                # Get result string and parse it.
                res_text = bloc_res_lines[line_id]

                # Isolate the text in Parenthesis.
                if ' (' in res_text:
                    res_text = res_text.replace(')', '').split(' (')
                    res_text = res_text[1]

                res_split = res_text.split(' ')

                # Init res variables.
                res_value = None
                res_unit = ''

                # Special case: keine Behinderung.
                if res_split[0] == 'keine' and line == 'Behinderung':
                    res_value = 0.0
                    res_unit = '%'

                # Special case: Schaden.
                elif ' - ' in res_text:
                    res_split = res_text.split(' - ')
                    res_value = [float(res_split[0]),
                                 float(res_split[1])]
                    res_unit = ''

                # Simple value, with optional unit.
                elif len(res_split) < 3:
                    res_value = float(res_split[0])
                    if len(res_split) == 2:
                        res_unit = res_split[1]

                # Store result.
                if not isinstance(res_value, list):
                    results_temp[res_name] = {'value': res_value,
                                              'unit': res_unit}
                else:
                    results_temp[res_name] = {'value_min': res_value[0],
                                              'value_max': res_value[1],
                                              'unit': res_unit}

    results.append(results_temp)


def export_results(results):
    # Join reports dir.
    reports_dir = os.path.join(os.getcwd(), 'reports')

    # Check if dir exists and create if not.
    if not os.path.exists(reports_dir):
        os.mkdir(reports_dir)

    # Create file name.
    report_path = datetime.now().strftime('%y%m%d_%H%M%S_eg_report.csv')

    # Ask for other file name.
    report_file_name = fd.asksaveasfilename(title="Auswertung speichern",
                                            filetypes=(('CSV Dateien', '*.csv'), ('All files', '*.*')),
                                            initialdir=reports_dir,
                                            initialfile=report_path)

    # Write the file contents.
    if report_file_name is not None:
        with open(report_file_name, 'w') as report_file:
            # Write header.
            for val in results[0]:
                report_file.write(val)
                if results[0][val]['unit'] != '':
                    report_file.write(f' - {results[0][val]["unit"]}')
                report_file.write(';')
            report_file.write('\n')

            # Write contents.
            for res_id, res in enumerate(results):
                for val in res:
                    if 'value' in res[val]:
                        report_file.write(f"{res[val]['value']};")
                    else:
                        report_file.write(f"{res[val]['value_min']}-{res[val]['value_max']};")
                report_file.write('\n')

        export_successful = True
    else:
        export_successful = False

    return export_successful


if __name__ == '__main__':
    stat_helper()
