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
        self.prop_name = prop_name

        if compare_symb == '<':
            self.predicate = lambda t: getattr(t, prop_name) < value
            self.acceptance_interval = (1, value - 1)
            self.rejection_interval = (value, 4000)
        else:
            self.predicate = lambda t: getattr(t, prop_name) > value
            self.acceptance_interval = (value + 1, 4000)
            self.rejection_interval = (1, value)

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
        self.previous_wls = []
        
    # for debugging
    def __repr__(self):
        return repr(vars(self))
    
class Search_State:
    def __init__(self, work_flow, interval_x, interval_m, interval_a, interval_s):
        self.work_flow = work_flow
        self.interval_x = interval_x
        self.interval_m = interval_m
        self.interval_a = interval_a
        self.interval_s = interval_s

def intersect_intervals(interval1, interval2) -> (int, int):
    (a1, b1) = interval1
    (a2, b2) = interval2
    return (max(a1, a2), min(b1, b2))

work_flows = []

with open('C:\\Users\\Lenovo\\source\\repos\\AdventOfCode23\\19\\input.txt', encoding="utf-8") as f:
    for line in f.readlines():
        if line == '\n':
            break

        label, rest = line.split('{')
        split = rest[:-2].split(',')
        rule_defs = split[:-1]
        terminal = split[-1]

        rules = []
        for rule_def in rule_defs:
            prop_name = rule_def[0]
            compare_symb = rule_def[1]
            rule_def_split = rule_def.split(':')
            destination_label = rule_def_split[1]
            value = int(rule_def_split[0][2:])

            rules.append(Rule(prop_name=prop_name, compare_symb=compare_symb, value=value, destination_label=destination_label))

        work_flows.append(Work_Flow(label=label, rules=rules, terminal_destination_label=terminal))
        continue

A = Work_Flow('A', [], 'A')
R = Work_Flow('R', [], 'R')

work_flows.append(A)
work_flows.append(R)

for work_flow in work_flows:
    if not work_flow in [A, R]:
        work_flow.terminal_destination = next(w for w in work_flows if w.label == work_flow.terminal_destination_label)
        work_flow.terminal_destination.previous_wls.append(work_flow)

    for rule in work_flow.rules:
        rule.destination = next(w for w in work_flows if w.label == rule.destination_label)
        if not work_flow in rule.destination.previous_wls:
            rule.destination.previous_wls.append(work_flow)

day2_result = 0
start = next(w for w in work_flows if w.label == 'in')

result_intervals = []
queue = [Search_State(A, (1, 4000), (1, 4000), (1, 4000), (1, 4000))]

#breakpoint()

while len(queue) > 0:
    state = queue.pop()
    #print(state.work_flow.label)

    if state.work_flow == start:
        result_intervals.append((state.interval_x, state.interval_m, state.interval_a, state.interval_s))

    for work_flow in state.work_flow.previous_wls:
        if work_flow.label == 'in':
            pass
        #print('inner')
        #print(work_flow.label)
        (x_lb, x_ub) = state.interval_x
        (m_lb, m_ub) = state.interval_m
        (a_lb, a_ub) = state.interval_a
        (s_lb, s_ub) = state.interval_s

        terminal_feasible = True

        for rule in work_flow.rules:
            if rule.destination == state.work_flow:
                # pontentially add state to queue with modified intervals s.t. rule accepts

                if rule.prop_name == 'x':
                    (new_x_lb, new_x_ub) = intersect_intervals((x_lb, x_ub), rule.acceptance_interval)
                    if new_x_ub >= new_x_lb:
                        queue.append(Search_State(work_flow, (new_x_lb, new_x_ub), (m_lb, m_ub), (a_lb, a_ub), (s_lb, s_ub)))

                if rule.prop_name == 'm':
                    (new_m_lb, new_m_ub) = intersect_intervals((m_lb, m_ub), rule.acceptance_interval)
                    if new_m_ub >= new_m_lb:
                        queue.append(Search_State(work_flow, (x_lb, x_ub), (new_m_lb, new_m_ub), (a_lb, a_ub), (s_lb, s_ub)))

                if rule.prop_name == 'a':
                    (new_a_lb, new_a_ub) = intersect_intervals((a_lb, a_ub), rule.acceptance_interval)
                    if new_a_ub >= new_a_lb:
                        queue.append(Search_State(work_flow, (x_lb, x_ub), (m_lb, m_ub), (new_a_lb, new_a_ub), (s_lb, s_ub)))

                if rule.prop_name == 's':
                    (new_s_lb, new_s_ub) = intersect_intervals((s_lb, s_ub), rule.acceptance_interval)
                    if new_s_ub >= new_s_lb:
                        queue.append(Search_State(work_flow, (x_lb, x_ub), (m_lb, m_ub), (a_lb, a_ub), (new_s_lb, new_s_ub)))

            # modify intervals s.t. rule rejects
        
            if rule.prop_name == 'x':
                (x_lb, x_ub) = intersect_intervals((x_lb, x_ub), rule.rejection_interval)
                if x_lb > x_ub:
                    terminal_feasible = False
                    break

                continue

            if rule.prop_name == 'm':
                (m_lb, m_ub) = intersect_intervals((m_lb, m_ub), rule.rejection_interval)
                if m_lb > m_ub:
                    terminal_feasible = False
                    break

                continue

            if rule.prop_name == 'a':
                (a_lb, a_ub) = intersect_intervals((a_lb, a_ub), rule.rejection_interval)
                if a_lb > a_ub:
                    terminal_feasible = False
                    break

                continue

            if rule.prop_name == 's':
                (s_lb, s_ub) = intersect_intervals((s_lb, s_ub), rule.rejection_interval)
                if s_lb > s_ub:
                    terminal_feasible = False
                    break
            
        if terminal_feasible and work_flow.terminal_destination == state.work_flow:
            queue.append(Search_State(work_flow, (x_lb, x_ub), (m_lb, m_ub), (a_lb, a_ub), (s_lb, s_ub)))


for interval in result_intervals:
    ((x_lb, x_ub), (m_lb, m_ub), (a_lb, a_ub), (s_lb, s_ub)) = interval
    day2_result += (x_ub - x_lb + 1) * (m_ub - m_lb + 1) * (a_ub - a_lb + 1) * (s_ub - s_lb + 1)

for interval in result_intervals:
    print(interval)

print('day 2 result: ', day2_result)