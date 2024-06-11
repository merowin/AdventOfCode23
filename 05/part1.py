import re

class MapEntry:
  def __init__(self, sourceStart: int, destinationStart: int, range: int):
    self.sourceStart = sourceStart
    self.destinationStart = destinationStart
    self.range = range

numberPattern = re.compile('[0-9]+')

def getNumbersInLine(line: str) -> list[int]:
    return list(map(lambda match: int(match[0]), re.finditer(numberPattern, line)))

def getDestination(mapEntries: list[MapEntry], source: int) -> int:
    for entry in mapEntries:
        if source >= entry.sourceStart and source - entry.sourceStart < entry.range:
            return entry.destinationStart + source - entry.sourceStart
    return source

seed_to_soil: list[MapEntry] = []
soil_to_fertilizer: list[MapEntry] = []
fertilizer_to_water: list[MapEntry] = []
water_to_light: list[MapEntry] = []
light_to_temperature: list[MapEntry] = []
temperature_to_humidity: list[MapEntry] = []
humidity_to_location: list[MapEntry] = []

maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, 
        water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]

### parse input

with open('input.txt', encoding="utf-8") as f:
    firstLine = f.readline()
    seeds = getNumbersInLine(firstLine)

    for line in f.readlines():
        if line == '\n':
            continue
        if line == 'seed-to-soil map:\n':
            map_in_construction = seed_to_soil
            continue
        if line == 'soil-to-fertilizer map:\n':
            map_in_construction = soil_to_fertilizer
            continue
        if line == 'fertilizer-to-water map:\n':
            map_in_construction = fertilizer_to_water
            continue
        if line == 'water-to-light map:\n':
            map_in_construction = water_to_light
            continue
        if line == 'light-to-temperature map:\n':
            map_in_construction = light_to_temperature
            continue
        if line == 'temperature-to-humidity map:\n':
            map_in_construction = temperature_to_humidity
            continue
        if line == 'humidity-to-location map:\n':
            map_in_construction = humidity_to_location
            continue

        numbers = getNumbersInLine(line)
        # I had source <-> destination swapped for a long time ...
        map_in_construction.append(MapEntry(numbers[1], numbers[0], numbers[2]))

### compute

minLocation = None

for seed in seeds:
    print('---------------------------')
    print(f'seed: {seed}')
    soil = getDestination(seed_to_soil, seed)
    print(f'soil: {soil}')
    fertilizer = getDestination(soil_to_fertilizer, soil)
    print(f'fertilizer: {fertilizer}')
    water = getDestination(fertilizer_to_water, fertilizer)
    print(f'water: {water}')
    light = getDestination(water_to_light, water)
    print(f'light: {light}')
    temperature = getDestination(light_to_temperature, light)
    print(f'temperature: {temperature}')
    humidity = getDestination(temperature_to_humidity, temperature)
    print(f'humidity: {humidity}')
    location = getDestination(humidity_to_location, humidity)
    print(f'location: {location}')

    if (minLocation == None or location < minLocation):
        minLocation = location

print(minLocation)