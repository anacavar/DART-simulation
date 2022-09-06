from tijelo import Tijelo

def ZOKG(m1, m2, v1, v2):
  # Savršeno neelastični sudar
  v_ukupno = (m1*v1+m2*v2)/(m1+m2)
  return v_ukupno

kuglica1 = Tijelo(1, 1)
kuglica1 = Tijelo(2, 1)

def move(dt = 0.1):
  pass
