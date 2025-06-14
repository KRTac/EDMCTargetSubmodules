#!/usr/bin/env python

from pynput.keyboard import KeyCode, Listener, Controller

try:
    import monitor
except ImportError:
    monitor = None

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from theme import theme
import myNotebook as nb
from config import config


listener = None
keyboard = Controller()

target = None
selected = None

is_active = tk.BooleanVar(value=True)

subsystem_keybind = tk.StringVar(value=config.get_str('subsystem_keybind') or 'z')
trigger_power_plant = tk.StringVar(value=config.get_str('trigger_power_plant') or 'k')
trigger_fsd = tk.StringVar(value=config.get_str('trigger_fsd') or '')
trigger_thrusters = tk.StringVar(value=config.get_str('trigger_thrusters') or '')

def plugin_start3(plugin_dir):
    global listener

    listener = Listener(handle_key_press)
    listener.start()

    return 'TargetSubmodules'


def plugin_stop():
    global listener

    if listener:
        listener.stop()
        listener = None


def journal_entry(cmdrname, is_beta, system, station, entry, state):
    global target, selected

    if not is_active.get() or entry['event'] != 'ShipTargeted':
        return

    if not entry['TargetLocked']:
        target = None
        selected = None
        return

    if 'Subsystem' in entry:
        selected = entry['Subsystem']

        if target:
            trigger_submodule_targeting()


def is_game_running():
    if not monitor:
        return True

    return monitor.monitor.game_running()


def trigger_submodule_targeting():
    global keyboard, subsystem_keybind, selected, target

    if selected and selected.startswith(target):
        target = None
    else:
        key = subsystem_keybind.get()[:1]

        keyboard.press(key)
        keyboard.release(key)


def handle_key_press(key):
    global target, is_active, trigger_power_plant, trigger_fsd, trigger_thrusters

    if not is_active.get() or not is_game_running():
        return

    trigger_targetting = False

    if key == KeyCode.from_char(trigger_power_plant.get()[:1]):
        target = '$int_powerplant'
        trigger_targetting = True
    elif key == KeyCode.from_char(trigger_fsd.get()[:1]):
        target = '$int_hyperdrive'
        trigger_targetting = True
    elif key == KeyCode.from_char(trigger_thrusters.get()[:1]):
        target = '$ext_drive'
        trigger_targetting = True

    if trigger_targetting:
        trigger_submodule_targeting()


def plugin_app(parent):
    global is_active

    frame = tk.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.grid(row=0, column=0, sticky='NSEW', columnspan=2)

    active_state_switch = tk.Checkbutton(
        frame, width=1, text='Target subsystems', variable=is_active,
        foreground='grey'
    )
    active_state_switch.grid(row=0, column=0, sticky=tk.EW + tk.N)

    theme.update(frame)

    return frame


def plugin_prefs(parent, cmdr, is_beta):
    global subsystem_keybind, trigger_power_plant, trigger_fsd, trigger_thrusters

    frame = nb.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

    nb.Label(frame, text='Subsystem targeting keybind:').grid(padx=10, pady=15, row=0, sticky=tk.E)
    nb.EntryMenu(frame, textvariable=subsystem_keybind, justify='center').grid(padx=10, pady=15, row=0, column=1, sticky=tk.W)

    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(columnspan=2, padx=20, pady=10, sticky=tk.EW)

    nb.Label(frame, text='Subsystem triggers').grid(columnspan=2, padx=40, pady=10, row=2, sticky=tk.EW)

    nb.Label(frame, text='Power plant:').grid(padx=10, row=3, sticky=tk.E)
    nb.EntryMenu(frame, textvariable=trigger_power_plant, justify='center').grid(padx=10, pady=5, row=3, column=1, sticky=tk.W)

    nb.Label(frame, text='FSD:').grid(padx=10, row=4, sticky=tk.E)
    nb.EntryMenu(frame, textvariable=trigger_fsd, justify='center').grid(padx=10, pady=5, row=4, column=1, sticky=tk.W)

    nb.Label(frame, text='Thrusters:').grid(padx=10, row=5, sticky=tk.E)
    nb.EntryMenu(frame, textvariable=trigger_thrusters, justify='center').grid(padx=10, pady=5, row=5, column=1, sticky=tk.W)

    nb.Label(
        frame,
        text='Make sure not to set any subsystem triggers the same as your Subsystem targeting keybind.'
    ).grid(columnspan=2, padx=10, pady=15, sticky=tk.EW)

    return frame


def prefs_changed(cmdr, is_beta):
    global subsystem_keybind, trigger_power_plant, trigger_fsd, trigger_thrusters

    subsystem_keybind.set(subsystem_keybind.get()[:1])
    config.set('subsystem_keybind', subsystem_keybind.get())

    trigger_power_plant.set(trigger_power_plant.get()[:1])
    config.set('trigger_power_plant', trigger_power_plant.get())

    trigger_fsd.set(trigger_fsd.get()[:1])
    config.set('trigger_fsd', trigger_fsd.get())

    trigger_thrusters.set(trigger_thrusters.get()[:1])
    config.set('trigger_thrusters', trigger_thrusters.get())
