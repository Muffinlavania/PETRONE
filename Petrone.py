#PETRONE GAME
#to run: go to command prompt and use py -m Petrone.py (in this folder)
#crash_sound = pygame.mixer.Sound("crash.wav")
#pygame.mixer.Sound.play(crash_sound)



import pygame,random,time,sys
from pygame.locals import *
#funcs
def rd(i1,i2):
  return random.randint(i1,i2)
def title(thi):
  pygame.display.set_caption(thi)
def screensize(size,size2):
  global screen
  screen = pygame.display.set_mode((size,size2))
screensize(1280,720)
HEIGHT = 720
WIDTH = 1280
def fill(color,default=screen): #can take RGB too?
  default.fill(color)
def selectfill(img, r=0, g=0, b=0):
  #input numbers below 120 for bext results (dont make them too extreme)
  for x in range(img.get_width()):
    for y in range(img.get_height()):
      a = img.get_at((x, y)) #r,g,b,a <- we get a
      img.set_at((x, y), pygame.Color(a[0] + r if a[0] + r<255 else 255, a[1] + g if a[1] + g < 255 else 255, a[2] + b if a[2] + b < 255 else 255, a[3])) #set things
  return img
def grayscale(img):
  for x in range(img.get_width()):
    for y in range(img.get_height()):
      av2 = img.get_at((x,y))
      av = (av2[0]+av2[1]+av2[2])//3
      img.set_at((x,y),pygame.Color(av,av,av,av2[3]))
  return img
def coords(X,Y):
  return pygame.Vector2(X,Y)
def anim(name,num,end='png'):
  return pygame.image.load(f"FILES/{name}/{name}-{num:05d}.{end}") #format num with 5 digits in total
def img(src):
  return pygame.image.load(f"IMAGES/{src}")
def check_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit()
def color(colo,wid=WIDTH,hei=HEIGHT):
  surf = pygame.Surface((wid,hei))
  surf.fill(colo)
  return surf
def flip(thi,x_flip=True,y_flip=False):
  return pygame.transform.flip(thi,x_flip,y_flip)
icon,bossicon = 'no existe','la fuenta de la juventud'
def obs():
  for i in objects:
    if (i.pos.right,i.pos.top) in [(212,673),(1272,3)]:
      bar_red = entity(color((209, 82, 79),140,40),((66,678) if i.pos.right<500 else (1126,8)))
      bar_green = entity(color((24, 207, 0),140,40),((66,678) if i.pos.right<500 else (1126,8)))
      show(bar_red.image, bar_red.pos)
      show(bar_green.image, bar_red.pos,(0,0,(round(140*((petrone_health if i.pos.right<500 else seg_health)/100))),40))
    show(i.image, i.pos, (80,0,50,50) if i in [icon,bossicon] else None) #health = 50x150

def up(thing=False):
  """Pass in either a pygame.Rect(x,y,width,height) or x,y,image"""
  if not thing:
    pygame.display.update()
  else:
    pygame.display.update(thing if type(thing) == pygame.rect.Rect else pygame.Rect(thing[0],thing[1],thing[2].get_width(),thing[2].get_height()))
def quit(prompt = "Finished game."):
  pygame.quit()
  input(prompt+"\n[Enter to close]")
  sys.exit()
def scale(thing,coors):
  return pygame.transform.scale(thing,coors)
def show(thing,where=(0,0),thingnightingi=None):
  screen.blit(thing,where,thingnightingi)
def sleep(tim=1000):
  li = list(i for i in range(20,500,5) if (tim/i < 50 and i==round(i)))[0]
  tim1 = time.time()
  for _ in range(li):
    key = pygame.key.get_pressed() #so it doesnt say unresponsive lol
    if key[pygame.K_v]:
      print(time.time()-tim1)
    check_events()
    pygame.time.delay(round(tim/li))

#big classes
class entity:
  def __init__(self, image, starting_cords = (0,0)):
    self.image = image
    self.height = self.image.get_height()
    self.pos = image.get_rect().move(starting_cords[0], starting_cords[1])
    self.width = self.image.get_width()
class Player:
  def __init__(self, image, speed):
    self.speed = speed
    entity.__init__(self,image) #yoinky sploinky entity
  def move(self, up=False, down=False, left=False, right=False):
    if disable_time<=0:
      if right: self.pos.right += self.speed
      elif left: self.pos.right -= self.speed
      if down: self.pos.top += self.speed
      elif up: self.pos.top -= self.speed
      
      if self.pos.right > WIDTH:
          self.pos.right = WIDTH
      if self.pos.right < self.width:
          self.pos.right = self.width
      if self.pos.top > HEIGHT-self.height:
          self.pos.top = HEIGHT-self.height
      if self.pos.top < 0:
          self.pos.top = 0

def touching(thing1:entity,thing2:entity,paddingtop=0,paddingsides=0): #both entites/players
  right = thing2.pos.right<thing1.pos.right-paddingsides and thing2.pos.right>thing1.pos.right-thing1.width+paddingsides
  left = thing2.pos.left>thing1.pos.left+paddingsides and thing2.pos.left<thing1.pos.left+thing1.width-paddingsides
  top = thing2.pos.top>thing1.pos.top+paddingtop and thing2.pos.top<thing1.pos.top+thing1.height-paddingtop
  bottom = thing2.pos.bottom<thing1.pos.bottom and thing2.pos.bottom>thing1.pos.bottom-thing1.height+paddingtop
  return  (right or left) and (top or bottom)
  
BOSSIN=False
def needed(AMO,start):
  q = AMO - round(round((time.time()-start)*1000),-1)
  return q if q>1 else 1
def SEG_WIN(backie=color((0,0,0))):
  screensize(1280,720)
  petrone.image = grayscale(pimage)
  heart = scale(img("heart.png"),(27,26))
  area = pygame.Rect(petrone.pos.left,petrone.pos.top,petrone.width,petrone.height)
  heartbreak = grayscale(scale(img("heartbreak.png"),(35,26)))
  heart_pos = (petrone.pos.right-60,petrone.pos.bottom-40)
  det = img("DETERMINATION2.png")
  show(backie,(0,0))
  up()
  sleep(1000)
  show(petrone.image,petrone.pos)
  up(area)
  sleep(2000)
  for i in range(20,256,2):
    heart.set_alpha(i)
    show(petrone.image,petrone.pos)
    show(heart,heart_pos)
    up(area)
    sleep(20)
  sleep(2000)
  for i in range(60):
    mult = 1 if i%2==0 else -1
    show(petrone.image,petrone.pos)
    show(heart,(heart_pos[0]+(i*mult)//3.5,heart_pos[1]))
    up(area)
    sleep(30-(i//3))
  pygame.mixer.Sound.play(pygame.mixer.Sound("FILES/heartbreak1.wav"))
  show(backie)
  show(petrone.image,petrone.pos)
  show(grayscale(heart),heart_pos)
  up(area)
  sleep(2000)
  behind = color((0,0,0))
  behind.set_alpha(150)
  pygame.mixer.Sound.play(pygame.mixer.Sound("FILES/heartbreak2.wav"))
  for i in range(255,-1,-3):
    if i==219:
      pygame.mixer.music.load("FILES/under.wav")
      pygame.mixer.music.play(-1)
    petrone.image.set_alpha(i)
    heartbreak.set_alpha(i)
    show(backie)
    show(petrone.image,petrone.pos)
    show(heartbreak,heart_pos)
    show(behind)
    show(det,(130,0),(0,0,det.get_width(),400))
    sleep(25)
    up()
  show(det,(130,0))
  up()
  sleep(6000)
def PET_WIN(backie=color((0,0,0))):
  screensize(1280,720)
  show(backie,(0,0))
  up()
  sleep(1000)
  start=time.time()
  seg_orig = scale(img("sogoian.png"),(160,200))
  for e in [pimage,scale(anim("PET",1,'jpg'),(400,250))]:
    show(backie,(0,0))
    show(e,((378,203) if e==pimage else (278,203)))
    show(seg_orig,(700,206))
    up()
    sleep(needed(2000,start) if e==pimage else needed(3000,start))
  seg_orig = flip(seg_orig)
  for i in range(1,146):
    show(backie,(0,0))
    show(seg_orig,(700,206))
    show(scale(anim("PET",i,'jpg'),(400,250)),(278,203))
    up()
    sleep(100 if (i>61 and i<76) or i>135 else 1000 if i==1 else 20)
  uhy = scale(anim("PET",145,'jpg'),(400,250))
  red_seg = flip(selectfill(scale(img("sogoian.png"),(160,200)),130,0,0))
  sleep(needed(11000,start))
  pygame.mixer.music.load("FILES/fire_idle.wav")
  pygame.mixer.music.set_volume(.3)
  pygame.mixer.music.play(-1)
  start=time.time()
  ned=0
  for i in range(300):
    show(backie,(0,0))
    show(uhy,(278,203))
    if i==200:
      pygame.mixer.Sound.play(pygame.mixer.Sound("FILES/minecraft.wav"))
    show(seg_orig if i<200 or i%25>12 else red_seg,(700,206))
    show(anim("fire",i%125+1,'png'),(680,230),(0,0,200,216))
    up(pygame.Rect(450,0,830,720))
    ned+=20
    sleep(needed(ned,start))
  win = img("winscreen.png")
  behind = color((0,0,0))
  behind.set_alpha(150)
  for i in range(20):
    red_seg.set_alpha(255-round(i*12.75))
    show(backie)
    show(scale(red_seg,(red_seg.get_width()*(i/5),red_seg.get_height())),(700,206))
    show(behind)
    show(win,(0,30))
    up()
    sleep(30)
    ned+=30
  sleep(needed(ned+7000,start))
def cutscene1(background,TXT,SKIP=False):
  global HEIGHT,WIDTH,petrone,seg,BOSSIN,seg_orig,colour,white_count,icon,bossicon,lagS
  lagS=60
  title("...")
  HEIGHT = 720
  WIDTH = 1280
  screensize(WIDTH,HEIGHT)
  p = img("boss.png")
  seg_orig=scale(p,(p.get_width()*1.2,p.get_height()*1.2))
  seg = entity(seg_orig)
  objects.append(seg)
  pygame.mixer.music.load('FILES/boss.mp3')
  pygame.mixer.music.set_volume(0.3)
  colour = (133,34,11)
  if not SKIP:
    pygame.mixer.music.play(-1)
    start = time.time()
    cut = pygame.transform.scale((cut2:=img("FIRSTCUT.png")),(WIDTH,HEIGHT))
    background.fill((0,0,0))
    for i in range(1,256,2):
      cut.set_alpha(i)
      screen.blit(background, (0, 0))
      screen.blit(cut, (0, 0))
      up()
      sleep(65)
    sleep(needed(13090,start))
    pygame.mixer.music.set_volume(0.35)
    background.fill((133,34,11))
    colour = (133,34,11)
    for i in range(40):
      cut = pygame.transform.scale(cut2,(WIDTH+9.5*i,HEIGHT+6.8*i))
      screen.blit(background,(0,0))
      screen.blit(cut,(-11.5*i,-6*i))
      screen.blit(background,((WIDTH*-1)+2.6*i,0))
      up()
      sleep(26)
    sleep(needed(14700,start))
    show(background,(0,0))
    show(img("SECONDCUT.png"),(-328.5,-154))
    up()
    sleep(needed(16450,start))
    show(background,(0,0))
    show(img("THIRDCUT.png"),(-328.5,-154))
    show(seg.image,(780,90))
    up()
    sleep(needed(17950,start))
    show(background,(0,0))
    show(img("FOURTHCUT.png"),(-328.5,-154))
    show(seg.image,(780,90))
    show(pim,(300,110))
    up()
    sleep(needed(18780,start))
    show(background,(0,0))
    show(seg.image,(780,90))
    show(pim,(300,110))
    up()
    sleep(needed(19010,start))
    show(background,(0,0))
    show(pim,(300,110))
    up()
    sleep(needed(19310,start))
    show(background,(0,0))
    up()
    sleep(needed(19610,start))
    petrone.image = pim
    for i in range(30,-1,-1):
      petrone.pos.right=740-14*i
      petrone.pos.top=500-3*i
      seg.pos.right=740+14*i
      seg.pos.top=0+3*i
      pim.set_alpha(210-7*i)
      seg_orig.set_alpha(210-7*i)
      show(pim,petrone.pos)
      show(seg_orig,seg.pos)
      up()
      sleep(20)
    petrone.image.set_alpha(255)
    seg.image.set_alpha(255)
    obs()
    up()
    sleep(needed(21280,start))
    show(background)
    obs()
    up()
    sleep(needed(22970,start))
    for i in range(30,-1,-1):
      HEIGHT-=i
      if i==0:
        HEIGHT-=30
      WIDTH-=i
      screensize(WIDTH,HEIGHT)
      sleep(20)
    up()
    show(color((0,0,0)),(0,0))
    show(TXT,(90,60))
    up()
    sleep(needed(24740,start))
    for i in range(30,-1,-1):
      HEIGHT+=i
      if i==0:
        HEIGHT+=30
      WIDTH+=i
      screensize(WIDTH,HEIGHT)
      sleep(15)
    show(background)
    obs()
    up()
    sleep(needed(25890,start))
  else:
    pygame.mixer.music.play(start = 25.86,loops=-1)
    petrone.pos.right=900
    petrone.pos.top=400
  white_count = 255
  BOSSIN=True
  
  #end cutscene
  icon = entity(scale(pim,(200,50)),(0,670))
  bossicon = entity(scale(seg.image,(200,50)),(1060,0))
  for i in [icon,bossicon,entity(scale(img("healthbar.png"),(152,50)),(60,673)),entity(scale(img("healthbar.png"),(152,50)),(1120,3))]:
    objects.append(i)
  title("The Fight to End Them All.")

colour=(160,132,173)

WHITE = color((255,255,255))
white_count = 256
clock = pygame.time.Clock()
lagS = 0
pimage = pygame.image.load("IMAGES/PETRONE.jpeg").convert_alpha()
pimage2 = pygame.image.load("IMAGES/PETRONE2.jpeg").convert_alpha()
busimage = img("bus.png")
#pygame.mixer.Sound.play(crash_sound)

petrone = Player(pimage, 10)
PETRONE_ORIGINAL_SIZE = pimage.get_size()

petrone_health = 100
seg_health = 100

#things to move
objects = [petrone]

boss_moves={
  0:(2,1),
  10:(3,1),
  20:(3,2),
  30:(4,1),
  40:(5,3),
  50:(6,3),
  60:(5,3),
  70:(4,2),
  80:(3,2),
  90:(2,2),
  100:(1,1),
}
dir_r = 1
dir_t = 1
fill((160,132,173))
def main():
  global screen,HEIGHT,WIDTH,colour,pim,FONT,white_count,SEG_COUNT,dir_t,dir_r,disable_time,petrone_health,seg_health
  pygame.init()
  HURT = pygame.mixer.Sound("FILES/hurt.wav")
  title("Mr.Petrone")
  lagS,frame=60,-1
  pim=pimage
  CURRENT_IMG = pimage
  FONT = pygame.font.Font('FILES/determination.ttf', 70)
  pygame.font.Font.set_underline(FONT,True)
  cs_text = FONT.render('The Battle for Petrone.', True, (255,255,255))
  SEG_COUNT=0
  HURT_COOL=0
  #game loops
  disable_time = 0
  while True:
    frame+=1
    white_count-=1
    
    #BOSS THINGS
    if not BOSSIN:
      if frame==-299:
        colour=(255,25,25)
      elif frame==0:
        colour=(160,132,173)
    else:
      if SEG_COUNT==0:
        SEG_COUNT=time.time() 
      if seg.pos.right > 900: dir_r = -1
      if seg.pos.right < 600: dir_r = 1
      if seg.pos.top < 10: dir_t = 1
      if seg.pos.top > 100: dir_t = -1
      seg.pos.right += boss_moves[round(seg.pos.right/3,-1)%100][0] * dir_r * 2
      seg.pos.top += boss_moves[round(seg.pos.right/3,-1)%100][1] * dir_t 
      
    
    #background
    backing = color(colour,WIDTH,HEIGHT)
    screen.blit(backing,(0,0))
    
    
    #print things
    petrone.image = pim
    if icon!='no existe':
      icon.image = scale(pim,(200,50))
    obs()
    
    if not BOSSIN:
      text = pygame.font.Font('FILES/determination.ttf', 32).render(f'R\T to drink petroleum, O\P to control the world [fps:{lagS}]', True, (0,255,0))
      screen.blit(text, (0,0))
    else:
      if white_count>0:
        WHITE.set_alpha(round(white_count))
        show(WHITE,(0,0))
      if touching(seg,petrone,20,20):
        if CURRENT_IMG!=pimage2:
          if HURT_COOL<0:
            pygame.mixer.Sound.play(HURT)
            HURT_COOL=3
          petrone_health -= 1
        else:
          seg_health -= 1
      
    k = pygame.key.get_pressed()
    if petrone_health <= 0:
      pygame.mixer.music.stop()
      SEG_WIN()
      quit("YOU DIED L")
    elif seg_health <= 0:  
      pygame.mixer.music.stop()
      PET_WIN()
      quit("YOU WON PETRONE OP")
    CURRENT_IMG = pimage2 if frame<0 else pimage
    pim=CURRENT_IMG 
    if k[pygame.K_UP] or k[pygame.K_w]:
      petrone.move(up=True)
    elif k[pygame.K_RIGHT] or k[pygame.K_d]:
      petrone.move(right=True)
      pim = pygame.transform.flip(CURRENT_IMG,True,False)
    elif k[pygame.K_DOWN] or k[pygame.K_s]:
      petrone.move(down=True)
    elif k[pygame.K_LEFT] or k[pygame.K_a]:
      petrone.move(left=True)
    if k[pygame.K_y] or k[pygame.K_u]:
      if not BOSSIN:
        backing = color(colour,1280,720)
        cutscene1(backing,cs_text,False if k[pygame.K_y] else True)
    if k[pygame.K_c]:
      frame=-300 if not BOSSIN else -100
    if k[pygame.K_r]:
      lagS=lagS+1 if lagS+1 !=300 else 299
    if k[pygame.K_t]:
      lagS=lagS-1 if lagS!=10 else 11
    if (k[pygame.K_o] or k[pygame.K_p]) and not BOSSIN:
      HEIGHT+=3 if k[pygame.K_p] else -3
      WIDTH+=3 if k[pygame.K_p] else -3
      screensize(WIDTH,HEIGHT)
    
    #for hitting X lol
    check_events()
        
    up() #passing nothing = full screen update
    lag_time = clock.tick(lagS) / 1000 #60 fps lol, lagS = time since last frame (1 = its fine, can be used in frame dependant animation?)
    HURT_COOL -= 1
    disable_time -= .5
#try:
main()
#except Exception as e:
#  print(f"\nERROR\n{e}\n\nye?")