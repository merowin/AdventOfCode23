import re

### preliminaries

class MapEntry:
  def __init__(self, sourceStart: int, destinationStart: int, range: int):
    self.sourceStart = sourceStart
    self.destinationStart = destinationStart
    self.range = range

  def __lt__(self, other):
    return self.sourceStart < other.sourceStart
  
  def getSourceEnd(self) -> int:
      return self.sourceStart + self.range - 1
  
  def getDestinationEnd(self) -> int:
      return self.destinationStart + self.range - 1
  
  def destinationOverlapsSourceOf(self, other) -> bool:
      return self.destinationStart <= other.getSourceEnd() and self.getDestinationEnd() >= other.sourceStart
  
  def getShift(self) -> int:
      return self.destinationStart - self.sourceStart

class SeedRange:
  def __init__(self, start: int, length: int):
    self.start = start
    self.length = length

numberPattern = re.compile('[0-9]+')

def getNumbersInLine(line: str) -> list[int]:
    return list(map(lambda match: int(match[0]), re.finditer(numberPattern, line)))

def getDestination(mapEntries: list[MapEntry], source: int) -> int:
    for entry in mapEntries:
        if source >= entry.sourceStart and source <= entry.getSourceEnd():
            return source + entry.getShift()
    return source

def getSource(mapEntries: list[MapEntry], destination: int) -> int:
    for entry in mapEntries:
        if destination >= entry.destinationStart and destination <= entry.getDestinationEnd():
            return destination - entry.getShift()
    return destination

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
    numbersInFirstLine = getNumbersInLine(firstLine)
    seedRanges: list[SeedRange] = []

    for i in range(len(numbersInFirstLine) // 2):
        seedRanges.append(SeedRange(numbersInFirstLine[2 * i], numbersInFirstLine[2 * i + 1]))

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
        # I had source <-> destination swapped for some time ...
        map_in_construction.append(MapEntry(numbers[1], numbers[0], numbers[2]))

for map in maps:
    map.sort()

### compute

minLocation = None

for seedRange in seedRanges:
    searchPoint = seedRange.start
    searchRange = seedRange.length

    while (searchPoint < seedRange.start + seedRange.length):
        mappedSearchPoint = searchPoint

        for map in maps:
            for entry in map:
                if mappedSearchPoint >= entry.sourceStart and mappedSearchPoint <= entry.getSourceEnd():
                    searchRange = min(searchRange, entry.getSourceEnd() - mappedSearchPoint + 1)
                    mappedSearchPoint = mappedSearchPoint + entry.getShift()
                    break
        
        if (minLocation == None or mappedSearchPoint < minLocation):
            minLocation = mappedSearchPoint
            print('new min location:')
            print(minLocation)
        
        searchPoint += searchRange

print(minLocation)