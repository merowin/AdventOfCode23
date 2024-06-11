def HASH(s: str) -> int:
    curr = 0
    for c in s:
        curr += ord(c)
        curr *= 17
        curr = curr % 256

    return curr

class Lense:
    def __init__(self, label: str, focus: int):
        self.label = label
        self.focus = focus

    # for debugging
    def __repr__(self):
        return repr(vars(self))

day2_result = 0
boxes: [[Lense]] = []
for i in range(256):
    boxes.append([])

with open('input.txt', encoding="utf-8") as f:
    seq = f.readline().strip().split(',')
    for s in seq:
        if '-' in s:
            label = s.split('-')[0]
            #print('- ', label)

            box: [Lense] = boxes[HASH(label)]
            lense_indices = [i for i, lense in enumerate(box) if lense.label == label]
            if len(lense_indices) > 0:
                box.pop(lense_indices[0])
            continue

        label, focus = s.split('=')
        focus = int(focus)

        box: [Lense] = boxes[HASH(label)]
        lense_indices = [i for i, lense in enumerate(box) if lense.label == label]

        if len(lense_indices) > 0:
            box[lense_indices[0]].focus = focus
            continue
        
        box.append(Lense(label, focus))

for i, box in enumerate(boxes):
    for j, lense in enumerate(box):
        day2_result += (i + 1) * (j + 1) * lense.focus

print('day 2 result ', day2_result)