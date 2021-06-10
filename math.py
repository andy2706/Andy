pin = 0
bedrag50 = 0
bedrag20 = 0
vijftig = 0
twintig = 0
aantal = 0

def count(pin):
  if pin < 20:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  if pin > 350:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  
  bedrag50 = pin % 50
  bedrag20 = bedrag50
  
  if bedrag20 < 20:
      twintig = 0
      
  if bedrag20 >= 20:
        bedrag20 = bedrag20 / 20
        bedrag20 = int(bedrag20)
        twintig = bedrag20
    
  bedrag50 = pin - bedrag50
  bedrag50 = bedrag50 / 50
  bedrag50 = int(bedrag50)
  vijftig = bedrag50

  if bedrag20 >=10 and bedrag20 <= 19:
      vijftig = vijftig - 1
      twintig = twintig + 3

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin    

aantal = count(60)
print(aantal)


