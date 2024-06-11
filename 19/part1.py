
class Machine_Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

class Rule:
    def __init__(self, prop_name, compare_symb, value, destination_label):
        self.destination_label = destination_label
        self.destination = None

        if compare_symb == '<':
            self.predicate = lambda t: getattr(t, prop_name) < value
        else:
            self.predicate = lambda t: getattr(t, prop_name) > value

    def apply(self, value):
        if self.predicate(value):
            return self.destination
        
        return None
    
    # for debugging
    def __repr__(self):
        return repr(vars(self))

class Work_Flow:
    def __init__(self, label, rules, terminal_destination_label):
        self.label = label
        self.rules = rules
        self.terminal_destination_label = terminal_destination_label
        self.terminal_destination = None
        
    # for debugging
    def __repr__(self):
        return repr(vars(self))

items = []
work_flows = []

with open('input.txt', encoding="utf-8") as f:
    reading_items = False

    for line in f.readlines():
        if line == '\n':
            reading_items = True
            continue

        if not reading_items:
            label, rest = line.split('{')
            split = rest[:-2].split(',')
            rule_defs = split[:-1]
            terminal = split[-1]

            #print(label, terminal, sep=' ')

            rules = []
            for rule_def in rule_defs:
                prop_name = rule_def[0]
                compare_symb = rule_def[1]
                rule_def_split = rule_def.split(':')
                destination_label = rule_def_split[1]
                value = int(rule_def_split[0][2:])

                #print(prop_name, compare_symb, value, destination_label, sep=' ')

                rules.append(Rule(prop_name=prop_name, compare_symb=compare_symb, value=value, destination_label=destination_label))

            work_flows.append(Work_Flow(label=label, rules=rules, terminal_destination_label=terminal))
            continue

        # reading items
        
        x = int(line.split('x=')[1].split(',')[0])
        m = int(line.split('m=')[1].split(',')[0])
        a = int(line.split('a=')[1].split(',')[0])
        s = int(line.split('s=')[1].split('}')[0])

        items.append(Machine_Part(x, m, a, s))

A = Work_Flow('A', [], 'A')
R = Work_Flow('R', [], 'R')

work_flows.append(A)
work_flows.append(R)

for work_flow in work_flows:
    work_flow.terminal_destination = next(w for w in work_flows if w.label == work_flow.terminal_destination_label)

    for rule in work_flow.rules:
        rule.destination = next(w for w in work_flows if w.label == rule.destination_label)

day1_result = 0
start = next(w for w in work_flows if w.label == 'in')

for item in items:
    current_wl = start

    while not current_wl in [A, R]:
        #print('current work flow: ', current_wl.label)
        applied_a_rule = False

        for rule in current_wl.rules:
            #print(rule.predicate(item))
            #print(rule.destination_label)
            #print(rule.destination.label)
            next = rule.apply(item)
            #print(next)

            if not next is None:
                current_wl = next
                applied_a_rule = True
                break

        if not applied_a_rule:
            current_wl = current_wl.terminal_destination

    if current_wl == A:
        day1_result += item.x + item.m + item.a + item.s

print('day 1 result: ', day1_result)