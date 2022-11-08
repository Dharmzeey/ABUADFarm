import csv
from users.models import Country, State, LGA


def run():
  f = open("excels/state_lga.csv")
  reader = csv.reader(f)
  country = Country.objects.create(name="NIGERIA")
  
  for row in reader:
    state, created = State.objects.get_or_create(name=row[1], country=country)
    lga = LGA.objects.create(name=row[0], country=country, state=state)
    lga.save()