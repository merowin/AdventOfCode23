# high pulse <-> True
# low pulse <-> False

class Module:
    def __init__(self, name, type_symb, destination_labels):
        self.name = name
        self.type_symb = type_symb
        self.destination_labels = destination_labels
        self.destinations = []
        self.memory = None

        # only relevant for conjunction modules
        self.input_modules = []

    def initialise_memory(self) -> None:
        match self.type_symb:

            # flip-flop
            case '%':
                # False <-> module is turned off
                self.memory = False
            
            # conjunction
            case '&':
                self.memory = [False] * len(self.input_modules)
    
    #for debugging
    def __repr__(self):
        d = vars(self)
        #d['destinations'] = []
        return repr(d)
    
class Transmission:
    def __init__(self, source, destination, pulse):
        self.source = source
        self.destination = destination
        self.pulse = pulse
    
    # for debugging
    def __repr__(self):
        return repr(vars(self))

broadcaster = None
modules = []
with open('input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        split = line.strip().split(' -> ')

        if split[0] == 'broadcaster':
            broadcaster = Module(name='broadcaster', type_symb='*', destination_labels=split[1].split(', '))
            modules.append(broadcaster)
            continue

        modules.append(Module(name=split[0][1:], type_symb=split[0][0], destination_labels=split[1].split(', ')))

for module in modules:
    for destination_label in module.destination_labels:

        if not any(True for m in modules if m.name == destination_label):
            destination_modul = Module(name=destination_label, type_symb='', destination_labels=[])
            modules.append(destination_modul)
        else:
            destination_modul = next(m for m in modules if m.name == destination_label)
        
        module.destinations.append(destination_modul)
        destination_modul.input_modules.append(module)

for module in modules:
    module.initialise_memory()

transmissions_queue = None
high_pulses = 0
low_pulses = 0

def transmit(transmission):
    global high_pulses
    global low_pulses

    if transmission.pulse:
        high_pulses += 1
    else:
        low_pulses += 1

    activated_module = transmission.destination

    #print('button' if transmission.source is None else transmission.source.name, '-high->' if transmission.pulse else '-low->', transmission.destination.name, sep=' ')

    match transmission.destination.type_symb:
        case '*':
            # broadcaster

            for module in activated_module.destinations:
                transmissions_queue.append(Transmission(source=activated_module, destination=module, pulse=False))

            return
        
        case '%':
            # flip-flop

            if transmission.pulse:
                return
            
            # switch on / off
            activated_module.memory = not activated_module.memory

            send_pulse = activated_module.memory
            for module in activated_module.destinations:
                transmissions_queue.append(Transmission(source=activated_module, destination=module, pulse=send_pulse))

            return
        
        case '&':
            # conjunction

            index = activated_module.input_modules.index(transmission.source)
            activated_module.memory[index] = transmission.pulse

            send_pulse = not all(activated_module.memory)
            for module in activated_module.destinations:
                transmissions_queue.append(Transmission(source=activated_module, destination=module, pulse=send_pulse))

initial_transmission = Transmission(source=None, destination=broadcaster, pulse=False)
repeats = 1000

for i in range(repeats):
    #print('*********************************')
    transmissions_queue = [initial_transmission]

    while (len(transmissions_queue) > 0):
        transmission = transmissions_queue.pop(0)

        transmit(transmission)

print('high pulses:', high_pulses,'low pulses:', low_pulses, sep=' ')

day1_result = low_pulses * high_pulses
print('day 1 result: ', day1_result)