from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, namedtuple

class ModuleType(Enum):
    BUTTON = 'button'
    BROADCASTER = 'broadcaster'
    FLIPFLOP = '%'
    CONJUNCTION = '&'
    OTHER = 'other'

class Pulse(Enum):
    HIGH = 'high'
    LOW = 'low'

class State(Enum):
    ON = 'on'
    OFF = 'off'

Signal = namedtuple('Signal', ['sender', 'pulse', 'module'])

@dataclass
class Module:
    type: ModuleType = ModuleType.OTHER
    input_pulses: dict[str, Pulse] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)
    state: State = State.OFF

def get_conjunction_module_output(signal: Signal, module: Module) -> Pulse | None:
    if all(pulse is Pulse.HIGH for pulse in module.input_pulses.values()):
        return Pulse.LOW
    else:
        return Pulse.HIGH

def get_flip_flop_module_output(signal: Signal, module: Module) -> Pulse | None:
    if signal.pulse is Pulse.HIGH:
        return
    if module.state is State.ON:
        module.state = State.OFF
        return Pulse.LOW
    else:
        module.state = State.ON
        return Pulse.HIGH

def get_broadcaster_module_output(signal: Signal, module: Module) -> Pulse | None:
    return signal.pulse

def get_button_module_output(signal: Signal, module: Module) -> Pulse | None:
    return Pulse.LOW

def get_other_module_ouput(signal: Signal, module: Module) -> Pulse | None:
    return

module_functions = {
    ModuleType.BUTTON: get_button_module_output,
    ModuleType.BROADCASTER: get_broadcaster_module_output,
    ModuleType.FLIPFLOP: get_flip_flop_module_output,
    ModuleType.CONJUNCTION: get_conjunction_module_output,
    ModuleType.OTHER: get_other_module_ouput
}

def get_all_modules(module_defs: list[str]) -> dict[str, Module]:
    all_modules = defaultdict(Module)
    for mod in module_defs:
        name, connections = mod.split(' -> ')
        if name.startswith('%'):
            name = name[1:]
            all_modules[name].type = ModuleType.FLIPFLOP
        elif name.startswith('&'):
            name = name[1:]
            all_modules[name].type = ModuleType.CONJUNCTION
        elif name == 'broadcaster':
            all_modules[name].type = ModuleType.BROADCASTER
        for conn in connections.split(', '):
            all_modules[name].outputs.append(conn)
            all_modules[conn].input_pulses[name] = Pulse.LOW
    all_modules['button'] = Module(ModuleType.BUTTON, outputs=['broadcaster'])
    return all_modules

def count_pulses(all_modules: dict[str, Module]) -> tuple[int, int]:
    '''
    first int is high count, second is low count
    '''
    start = Signal('button', Pulse.LOW, 'broadcaster') 
    signals = [start]
    pulse_counts = {
        Pulse.HIGH: 0,
        Pulse.LOW: 0
    }
    while signals:
        curr_sig = signals.pop(0)
        curr_module = all_modules[curr_sig.module]
        curr_module.input_pulses[curr_sig.sender] = curr_sig.pulse
        pulse_to_send = module_functions[curr_module.type](curr_sig, curr_module)
        pulse_counts[curr_sig.pulse] += 1
        if pulse_to_send:
            for name in curr_module.outputs:
                new_signal = Signal(curr_sig.module, pulse_to_send, name)
                signals.append(new_signal)
    return pulse_counts[Pulse.HIGH], pulse_counts[Pulse.LOW]

def main():
    with open('inputs.txt') as file:
        module_defs = [line.strip() for line in file]
    all_modules = get_all_modules(module_defs)
    high_total, low_total = 0, 0
    for i in range(1000):
        high_count, low_count = count_pulses(all_modules)
        high_total += high_count
        low_total += low_count
    print(f'Part 1: {high_total * low_total}')
    print(f'Part 2: Not yet implemented')

if __name__ == '__main__':
    main()
