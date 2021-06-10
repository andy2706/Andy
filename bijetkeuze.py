pin = 0
bedrag50 = 0
bedrag20 = 0
vijftig = 0
twintig = 0
aantal = 0

# prioriteit op biljetten van 50

def prio50(pin):
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

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin    

aantal = prio50(60)
print(aantal)

pin = 0
bedrag50 = 0
bedrag20 = 0
vijftig = 0
twintig = 0
aantal = 0


# prioriteit op bijetten van 20

def prio20(pin):
  if pin < 20:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  if pin > 350:
        vijftig = 0
        twintig = 0
        return vijftig , twintig
  
  bedrag50 = pin % 20

  twintig = int(pin/20)

  if int(pin/20) > 9:
      bedrag50 = pin - 180
      twintig = 9
    #   bedrag50 = pin

  if bedrag50 < 50:
      vijftig = 0
      
  if bedrag50 > 50:
    bedrag50 = pin - bedrag50
    bedrag50 = bedrag50 / 50
    bedrag50 = int(bedrag50)
    vijftig = bedrag50

  pin = 50 * vijftig + 20 * twintig 

  return vijftig , twintig, pin   

aantal = prio20(60)
print(aantal)

pin = 0
bedrag50 = 0
bedrag20 = 0
vijftig = 0
twintig = 0
aantal = 0


# standaard operatie

def geenVoorkeur(pin):
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

aantal = geenVoorkeur(60)
print(aantal)
