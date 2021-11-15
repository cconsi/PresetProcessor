import os
import sys
import bs4
import PySimpleGUI as simplegui


def parse_preset_html(filepath: str) -> str:
    try:
        with open(filepath) as f:
            doc = bs4.BeautifulSoup(f, 'html.parser')
    except FileNotFoundError as fnf:
        print('file does not exist')
    except Exception as e:
        print(e)

    mod_list = "-mod=\""
    links = doc.find_all('a')
    for item in links:
        link = item['href']
        id = link.split('id=')[1]
        tag = "@" + id + ";"
        mod_list += tag
    mod_list += "\""
    return mod_list


def process(gui, inputs):
    command_line_string = ""
    defaults = "-noPause -noSound -enableHT -loadMissionToMemory -world=empty"
    ip = '-ip=' + inputs['-ip-']
    port = '-port=' + inputs['-port-']
    mem = '-maxMem=' + inputs['-memory-']
    config = '-config=' + inputs['-config-']
    mods = parse_preset_html(inputs['-preset-'])
    command_line_string += f"{ip} {port} {mem} {config} {mods}"
    if inputs['-profile-']:
        profile = '-profiles=' + inputs['-profile-']
        command_line_string += f" {profile}"
    if inputs['-defaults-']:
        command_line_string += f" {defaults}"

    preset_name = inputs['-preset-'].split('/')[-1].split('.')[0]
    with open(os.path.join(inputs['-output-'], f"{preset_name}_commandlineargs.txt"), "w") as wf:
        wf.write(command_line_string)


def gui_init() -> simplegui.Window:
    simplegui.theme('DarkAmber')
    title = 'Watchdog\'s Arma 3 Server Command Line Generator'
    inputs_layout = [ [simplegui.Text('Server Information')],
                      [simplegui.Text('IP Address:'), simplegui.InputText(size=(25, 1), enable_events=True, key='-ip-')],
                      [simplegui.Text('Port:'), simplegui.InputText(size=(25, 1), enable_events=True, key='-port-')],
                      [simplegui.Text('Max Memory:'), simplegui.InputText('8192', size=(25, 1), enable_events=True, key='-memory-')],
                      [simplegui.Text('Config File:'), simplegui.InputText('default.cfg', size=(25, 1), enable_events=True, key='-config-')],
                      [simplegui.Text('Arma Profile:'), simplegui.InputText(size=(25, 1), enable_events=True, key='-profile-')],
                      [simplegui.Checkbox('Include ServerBlend Default Startup Values?', enable_events=True, key='-defaults-')]
                    ]
    preset_layout = [ [simplegui.Text('Select Mod Preset File'),
                        simplegui.In(disabled=True, text_color='black', size=(25, 1), enable_events=True, key='-preset-'),
                        simplegui.FileBrowse()],
                      [simplegui.Text('Select Output Directory'),
                        simplegui.In(disabled=True, text_color='black', size=(25,1), enable_events=True, key='-output-'),
                        simplegui.FolderBrowse()],
                      [simplegui.Button('Process', key='-process-', disabled=True)]
                    ]
    layout = [[simplegui.Column(inputs_layout), simplegui.VSeperator(), simplegui.Column(preset_layout)]]
    margins = (10,10)
    gui = simplegui.Window(title=title, layout=layout, margins=margins)
    return gui


def validate(gui, inputs):
    ip = inputs['-ip-']
    port = inputs['-port-']
    mem = inputs['-memory-']
    defaults = inputs['-defaults-']
    config = inputs['-config-']
    preset = inputs['-preset-']
    output = inputs['-output-']
    if all([ip, port, mem, config, preset, output]):
        gui['-process-'].update(disabled=False)
        return True
    else:
        gui['-process-'].update(disabled=True)
        return False


def main():

    # create gui window and main event loop
    gui = gui_init()
    while True:
        event, values = gui.read()

        if event == "-process-":
            if validate(gui, values):
                process(gui, values)
        elif event == simplegui.WIN_CLOSED:
            gui.close()
            break
        else:
            validate(gui, values)


if __name__ == '__main__':
    main()
