
#imports
import pygame 
import random
import math
import csv
import pickle
from os import path
from time import sleep
from tkinter import*
from tkinter import messagebox
pygame.init()
pygame.mixer.init()



l=[]
def update_score(l):
    f=open("High_score.csv","r",newline="\r\n")
    r=csv.reader(f) 
    n=[]
    for i in r:
        if i[0]==l[0]:
            i.clear()
            i.extend(l)
        n.append(i)
    else:
        f=open("High_score.csv","w",newline="")
        w=csv.writer(f)
        w.writerows(n)
        f.close()
    
    
def add_high_score(a):
    f=open("High_score.csv","r",newline="\r\n")
    r=csv.reader(f)
    for i in r:
        if i[0]==a:
            l.extend(i)
    f.close()
            
def add_high_data(a):
 
    f=open("High_score.csv","a",newline="")
    l=[a,0,0,0,0,0,0,0]
    c=csv.writer(f)
    c.writerow(l)
    f.close()

#csv
def add_user(a,b):
    f=open("User.csv","a",newline="")
    w=csv.writer(f)
    l=[a,b]
    w.writerow(l)

    f.close()


def check_users(username,password):
    global user,u
    f=open("User.csv","r",newline="\r\n")
    r=csv.reader(f)
    for i in r:
        if i==[]:
           return False
        elif i[0]==username and i[1]==password:
            u=username
            return True
    else:
        return False
        
        
#login
login_done=True
if login_done:
    def login():
            global root,login_done,username
            username=entry1.get()
            password=entry2.get()
       
            if (username=="" or password==""):
                messagebox.showinfo("","Blank Not Allowed")
                
            elif check_users(entry1.get(),entry2.get()):
                messagebox.showinfo("","login successful")
                add_high_score(username)
                root.destroy()
                login_done=False
                
            else:
                messagebox.showinfo("","Incorrect username or password")
    def create():
                    global entry1,entry2
                    a=check_users(entry1.get(),entry2.get())
                    if not a:
                        messagebox.showinfo("","user create successfully")
                        add_user(entry1.get(),entry2.get())
                        add_high_data(entry1.get())

                    if a:
                        messagebox.showinfo("","user already created!!!")
    root=Tk()
    root.title("GAME LOGIN")
    root.geometry("300x200")
        
    global entry1
    global entry2
        
    Label(root,text="Username : ").place(x=20,y=20)
    Label(root,text="Password : ").place(x=20,y=70)
        
    entry1=Entry(root,bd=5)
    entry1.place(x=140,y=20)
    
    entry2=Entry(root,bd=5,show="*")
    entry2.place(x=140,y=70)
        
    Button(root,text="Login",command=login,height=3,width=13,bd=6).place(x=30,y=120)
    Button(root,text="Create",command=create,height=3,width=13,bd=7).place(x=150,y=120)
    
    root.mainloop()

if login_done:
    add_high_score()

#assets
img_dir =path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'music')

#creating music
bulletSound = pygame.mixer.Sound(path.join(sound_folder,'bullet.wav'))
hitSound = pygame.mixer.Sound(path.join(sound_folder,'hit.wav'))
crashSound = pygame.mixer.Sound(path.join(sound_folder,'crash.wav'))
game_overSound=pygame.mixer.Sound(path.join(sound_folder,"Game over.ogg"))
packetSound=pygame.mixer.Sound(path.join(sound_folder,"packet.wav"))
one_heartSound=pygame.mixer.Sound(path.join(sound_folder,"heart.wav"))
packetSound.set_volume(0.3)
bulletSound.set_volume(0.5)
hitSound.set_volume(0.3)
crashSound.set_volume(0.4)
game_overSound.set_volume(0.7)


#screen developement
if not login_done:
    screen_width=1000
    screen_height=650
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("SPACE GAMES")
    pygame.display.set_icon(pygame.image.load(path.join(img_dir,"rocket.png")))

#creating player
player_x=20
player_y=300
player_x_change=4
player_y_change=4
player=pygame.image.load(path.join(img_dir,"spaceship.png")).convert_alpha()
player_shield=pygame.image.load(path.join(img_dir,"spaceship_shield.png")).convert_alpha()
player_rocket=pygame.image.load(path.join(img_dir,"spaceship_rocket.png")).convert_alpha()


#asteroids
asteroid_img=[]
asteroid_x=[]
asteroid_y=[]
asteroid_change=[]
asteroid_scale=[]
asteroid_update=[]
        
number_of_asteroids=12
for i in range(number_of_asteroids ):
        asteroid_x.append(random.randint(1500,1600))
        asteroid_y.append(random.randint(0,650))
        asteroid_change.append(random.uniform(4,5))
        asteroid_scale.append(random.uniform(1,2))
               
asteroid_list=["1.png","2.png","3.png","4.png","1.png","2.png","3.png","4.png","1.png","2.png","3.png","4.png"]
for image in asteroid_list:
    asteroid_img.append(pygame.image.load(path.join(img_dir,image)).convert_alpha())
for i in range(number_of_asteroids):
           x=asteroid_img[i]
           w=asteroid_img[i].get_width()
           h=asteroid_img[i].get_height()
           y=asteroid_scale[i]
           update=pygame.transform.scale(x,(w*y,h*y))
           asteroid_update.append(update)
def create_asteroid(asteroid_x,asteroid_y,i):
        global asteroid_update
        screen.blit(asteroid_update[i],(asteroid_x,asteroid_y))


#collision of player with asteroids
def asteroid_collision(x,y,a,b):
    global run 
    global n
    d=math.sqrt((x-a)**2+(y-b)**2)
    if d<=60:
        return True
    
    else:
        return False
load=500
max_load=500
text=pygame.font.Font("freesansbold.ttf",100)    
loading_text=text.render("LOADING",True,(255,255,255))

def loading_screen(l):
    global load,max_load,loading,main_screen
    ratio=load/max_load
    screen.fill((0,0,0))
    screen.blit(loading_text,(250,225))
    pygame.draw.rect(screen,"green",(250,325,500,50))
    sleep(1)
    load-=l
    pygame.draw.rect(screen,"white",(250,325,500*ratio,50))
    if load<=0:
        loading=False
        return True        
    
#score 

score=0    
pygame.font.init()
font=pygame.font.Font("freesansbold.ttf",50)
font_x=450
font_y=0
def display_score(x,y):
    global font
    global score
    score_img=font.render("SCORE:"+str(score),True,(255,255,255))
    screen.blit(score_img,(x,y))

#creating bg 
bg_img=pygame.image.load(path.join(img_dir,"622.jpg")).convert_alpha()
bg=pygame.transform.scale(bg_img,(1000,650))
s=0

start_img=pygame.image.load(path.join(img_dir,"bg_main.png")).convert_alpha()
s_img=pygame.transform.scale(start_img,(1000,650))

crash_c=pygame.image.load(path.join(img_dir,"crash.png")).convert_alpha()
crash_img=pygame.transform.scale(crash_c,(1000,650))

#creating bullets 
bullet_img=pygame.image.load(path.join(img_dir,"bullet.png")).convert_alpha()
bullet_x=0
bullet_y=0
bullet_change_x=10     
bullet_state="load"
def bullet_position(player_x,player_y):
    global bullet_x
    global bullet_y
    global bullet_state
    if bullet_state=="load":
        bullet_x=player_x+1
        bullet_y=player_y+27
last_shot=0         
def bullet_fired():
    global last_shot
    global bullet_state 
    global bullet_x
    global bullet_y        
    bullet_state="fire"
    screen.blit(bullet_img,(bullet_x+60,bullet_y+27))
    last_shot=pygame.time.get_ticks()

def bullet_collision(x,y,a,b):
     global score
     d=math.sqrt((x-a)**2+(y-b)**2)
     if d<=60:
         return True
         score+=10
     else:
         return False
bullets=100
def bullet_number(bullets):
    bullet_display=pygame.image.load(path.join(img_dir,"bullets.png"))
    screen.blit(bullet_display,(300,0))
pygame.font.init()
f=pygame.font.Font("freesansbold.ttf",27)
f_x=350
f_y=10
def display_bullets(x,y):
    global f
    global bullets
    bullet_img=f.render(str(bullets),True,(255,255,255))
    screen.blit(bullet_img,(x,y))
 
#creating hearts
n=0
def hearts():
      global start
      global n 
      global player_x
      global player_y
      global run
      heart0=pygame.image.load(path.join(img_dir,"heart0.png")).convert_alpha()
      heart1=pygame.image.load(path.join(img_dir,"heart1.png")).convert_alpha()
      heart2=pygame.image.load(path.join(img_dir,"heart2.png")).convert_alpha()
      heart3=pygame.image.load(path.join(img_dir,"heart3.png")).convert_alpha()
      heart4=pygame.image.load(path.join(img_dir,"heart4.png")).convert_alpha()
      heart5=pygame.image.load(path.join(img_dir,"heart5.png")).convert_alpha()
      if n==0:
          screen.blit(heart5,(0,0))
      elif n==1:
          screen.blit(heart4,(0,0))
      elif n==2:
          screen.blit(heart3,(0,0))         
      elif n==3:
          screen.blit(heart2,(0,0))
      elif n==4:
           screen.blit(heart1,(0,0))
      elif n==5:
         screen.blit(heart0,(0,0))
         start="No"
         game_over()
        
#packets

packet=pygame.image.load(path.join(img_dir,"packet.png")).convert_alpha()
packet2=pygame.image.load(path.join(img_dir,"packet2.png")).convert_alpha()
packet3=pygame.image.load(path.join(img_dir,"packet3.png")).convert_alpha()
packet_x=random.randint(1100,1200)
packet_y=(random.randint(100,600))
packet_x_change=(random.uniform(1,2))
packet_x2=random.randint(1100,1200)
packet_y2=(random.randint(100,600))
packet_x_change2=(random.uniform(1,2))
packet_x3=random.randint(1100,1200)
packet_y3=(random.randint(100,600))
packet_x_change3=(random.uniform(1,2))

def create_packet():
    global packet
    global packet_x
    global packet_y
    screen.blit(packet,(packet_x,packet_y))
def create_packet2():
    global packet2
    global packet_x2
    global packet_y2
    screen.blit(packet2,(packet_x2,packet_y2))
def create_packet3():
    global packet3
    global packet_x3
    global packet_y3
    screen.blit(packet3,(packet_x3,packet_y3))

#packet collision
def packet_collision(x,y,a,b):
    global n
    d=math.sqrt((x-a)**2+(y-b)**2)
    if d<=60 :
        return True
    else:
        return False
      
#game over
gameover=False
def game_over():
    global score
    global game_overSound
    global run,main_screen,alien_battle,asteroid_escape,crash
    game_overSound.play()
    pygame.mixer.music.stop()
    pygame.font.init()
    font=pygame.font.Font("freesansbold.ttf",80)
    font2=pygame.font.Font("freesansbold.ttf",30)
    over_x=250
    over_y=250
    restart_x=130
    restart_y=350
    game_over=font.render("GAME OVER",True,(255,0,0))
    restart_msg=font2.render("Press c to restart the game or q to quit the game",True,(255,255,255))
    screen.blit(game_over,(over_x,over_y))
    screen.blit(restart_msg,(restart_x,restart_y))
    gameover=True
    main_screen=False
    alien_battle=False
    asteroid_escape=False
    crash=True
    compare_score()
    score_board()

def compare_score():
    global l,score,asteroid_destroyed,alien_killed,commander_killed,bullets_shot,packets_taken,hearts_lost
    if int(l[1])<score:
        l[1]=score
        l[2]=asteroid_destroyed
        l[3]=alien_killed
        l[4]=commander_killed
        l[5]=bullets_shot
        l[6]=packets_taken
        l[7]=hearts_lost
    update_score(l)
        
sc=pygame.image.load(path.join(img_dir,"score_bg.png"))
score_bg=pygame.transform.scale(sc,(1000,650))

def score_board():
        global score_bg,main_screen,s_board,l
        global asteroid_destroyed,alien_killed,commander_killed,bullets_shot,packets_taken,hearts_lost
        if main_screen==False and s_board==True:
            a=score
            b=asteroid_destroyed
            c=alien_killed
            d=commander_killed
            e=bullets_shot
            z=packets_taken
            g=hearts_lost
            screen.blit(score_bg,(0,0))
            pygame.font.init()
            f=pygame.font.Font("freesansbold.ttf",27)
            score_img=f.render(str(a),True,(255,255,255))
            screen.blit(score_img,(162,268))
            aster_img=f.render(str(b),True,(255,255,255))
            screen.blit(aster_img,(210,301))
            bul_img=f.render(str(e),True,(255,255,255))
            screen.blit(bul_img,(180,403))
            pac_img=f.render(str(z),True,(255,255,255))
            screen.blit(pac_img,(215,441))
            hea_img=f.render(str(g),True,(255,255,255))
            screen.blit(hea_img,(243,472))
            alie_img=f.render(str(c),True,(255,255,255))
            screen.blit(alie_img,(170,335))
            com_img=f.render(str(d),True,(255,255,255))
            screen.blit(com_img,(225,372))
            
            a1=l[1]
            b1=l[2]
            c1=l[3]
            d1=l[4]
            e1=l[5]
            z1=l[6]
            g1=l[7]
            h_score_img=f.render(str(a1),True,(255,255,255))
            screen.blit(h_score_img,(680,260))
            h_aster_img=f.render(str(b1),True,(255,255,255))
            screen.blit(h_aster_img,(740,294))
            h_bul_img=f.render(str(e1),True,(255,255,255))
            screen.blit(h_bul_img,(710,395))
            h_pac_img=f.render(str(z1),True,(255,255,255))
            screen.blit(h_pac_img,(745,430))
            h_hea_img=f.render(str(g1),True,(255,255,255))
            screen.blit(h_hea_img,(770,462))
            h_alie_img=f.render(str(c1),True,(255,255,255))
            screen.blit(h_alie_img,(700,328))
            h_com_img=f.render(str(d1),True,(255,255,255))
            screen.blit(h_com_img,(762,363))
        
        
           
#restart
def restart():
    global player_x,player_y
    global asteroid_x, asteroid_y
    global number_of_asteroids
    global n,score,bullets
    global bgSound
    global packet_x,packet_y,packet_x2,packet_y2,packet_x3,packet_y3
    global bullet_x,bullet_y
    global game_overSound
    global packet4
    global a,b,c,d,e,g
    global no_rocket,no_bullet,no_heart,no_shield
    global alien_x, alien_y
    global number_of_aliens
    global alien_bullet_state,commander
    global commander_x,commander_y,hp
    global  score,asteroid_destroyed,alien_killed,commander_killed,bullets_shot,packets_taken,hearts_lost
    hp=250
    pygame.mixer.music.play(-1)
    commander_x=1000
    commander_y=350
    commander=False
    game_overSound.stop() 
    bullet_x=player_x
    bullet_y=player_y
    asteroid_destroyed=0
    alien_killed=0
    commander_killed=0
    bullets_shot=0
    packets_taken=0
    hearts_lost=0 
    a=b=c=d=e=g=z=0
    no_bullet=no_heart=no_rocket=no_shield=False
    player_x=20
    player_y=300
    n=0
    score=0
    bullets=100
    packet_x=random.randint(1100,1200)
    packet_y=(random.randint(100,600))
    packet_x2=random.randint(1100,1200)
    packet_y2=(random.randint(100,600))
    packet_x3=random.randint(1100,1200)
    packet_y3=(random.randint(100,600))
    for i in range(number_of_asteroids):
        asteroid_x[i]=random.randint(1000,1100)
        asteroid_y[i]=random.randint(0,650)
    for i in range(number_of_aliens):
          alien_x[i]=random.randint(1000,1100)
          alien_y[i]=random.randint(0,650)
          alien_bullet_state[i]="load"  
    
creating_asteroids=True
creating_packets=True

     
#pause
pause=False
#clock
clock=pygame.time.Clock()   

begin="no"
start="no"

#timer
shield_time=0
b=0
no_shield=True
bullet_time=0
c=0
no_bullet=False
heart_time=0
d=0
no_heart=False
noshield=False
e=0
noshield_time=0
g=0

heart_down=False
z=0

one_heart=True
#main loop
run=True
#aliens
alien_img=[]
alien_x=[]
alien_y=[]
alien_change=[]
alien_list=[]

number_of_aliens=12
for i in range(number_of_aliens):
        alien_x.append(random.randint(1500,1600))
        alien_y.append(random.randint(0,650))
        alien_change.append(random.uniform(3,4))

aliens=["alien1.png","alien2.png","alien3.png","alien4.png","alien5.png","alien6.png"
        ,"alien1.png","alien2.png","alien3.png","alien4.png","alien5.png","alien6.png"]

for images in aliens:
    alien_list.append(pygame.image.load(path.join(img_dir,images)).convert_alpha())


def create_alien(alien_x,alien_y,i):
        global alien_list
        screen.blit(alien_list[i],(alien_x,alien_y))
        
#collision of player with aliens
def alien_collision(x,y,a,b):
    global run 
    global n
    d=math.sqrt((x-a)**2+(y-b)**2)
    if d<=60:
        return True
    
    else:
        return False
         
alien_bullet_img=[]
alien_bullet_x=[]
alien_bullet_y=[]
alien_bullet_change_x=[]     
alien_bullet_state=[]

for i in range(number_of_aliens):
    alien_bullet_img.append(pygame.image.load(path.join(img_dir,"alien_bullet.png")))
    alien_bullet_x.append(0.0)
    alien_bullet_y.append(0.0)
    alien_bullet_change_x.append(random.uniform(7,8)) 
    alien_bullet_state.append("load")
    
def alien_bullet_position(alien_x,alien_y,i):
    global alien_bullet_x
    global alien_bullet_y
    global alien_bullet_state
    if alien_bullet_state[i]=="load":
        alien_bullet_x[i]=alien_x+1
        alien_bullet_y[i]=alien_y+27

def alien_bullet_fired(i):
    global alien_bullet_state 
    global alien_bullet_x
    global alien_bullet_y        
    alien_bullet_state[i]="fire"
    screen.blit(alien_bullet_img[i],(alien_bullet_x[i]+40,alien_bullet_y[i]+20))

def alien_bullet_collision(x,y,a,b):
     d=math.sqrt((x-a)**2+(y-b)**2)
     if d<=60:
        return True
     else:
         return False
 
        
#commanders
com1=pygame.image.load(path.join(img_dir,"commander1.png"))
com2=pygame.image.load(path.join(img_dir,"commander2.png"))
com3=pygame.image.load(path.join(img_dir,"commander3.png"))
w=com1.get_width()
h=com1.get_height()
commander1=pygame.transform.scale(com1,(w*1,h*1))
commander2=pygame.transform.scale(com2,(w*1,h*1))
commander3=pygame.transform.scale(com3,(w*1,h*1))

com=random.randint(1,3)
commander_x=1000
commander_y=325

def create_commmander():
    global score,com,commander1,commander2,commander3
    global commander_x,commander_y
    if com==1:
        screen.blit(commander1,(commander_x,commander_y))
    if com==2:
        screen.blit(commander2,(commander_x,commander_y))
    if com==3:
        screen.blit(commander3,(commander_x,commander_y))

commander_rocket_img=pygame.image.load(path.join(img_dir,"commander_rocket.png"))
commander_rocket_x=0
commander_rocket_y=0
commander_rocket_change_x=8
commander_rocket_state="load"
def commander_rocket_position(commander_x,commander_y):
    global commander_rocket_x
    global commander_rocket_y
    global commander_rocket_state
    if commander_rocket_state=="load":
        commander_rocket_x=commander_x+5
        commander_rocket_y=commander_y+80
         
def commander_rocket_fired():
    global commander_rocket_state 
    global commander_rocket_x
    global commander_rocket_y        
    commander_rocket_state="fire"
    screen.blit(commander_rocket_img,(commander_rocket_x-25,commander_rocket_y+35))
   

def commander_rocket_collision(x,y,a,b):
    
     d=math.sqrt((x-a)**2+(y-b)**2)
     if d<=60:
         return True
       
     else:
         return False

def commander_bullet_collision(x,y,a,b):
    
     d=math.sqrt((x-a)**2+(y-b)**2)
     if d<=60:
         return True
       
     else:
         return False
def bullet_rocket_collision():
    d=math.sqrt((commander_rocket_x-bullet_x)**2+(commander_rocket_y-bullet_y)**2)
    if d<=60:
        return True
    else:
        return False

def player_commander_collision(x,y,a,b):
     d=math.sqrt((x-a)**2+(y-b)**2)
     if d<=60:
         return True
       
     else:
         return False



c_health=pygame.font.Font("freesansbold.ttf",20)    
commander_health=c_health.render("COMMANDER",True,(255,0,0))
max_hp=250
hp=250

def commander_health_draw():
    global c_health,commander_health,max_hp,hp
    hp_ratio=hp/max_hp
    screen.blit(commander_health,(700,80))
    pygame.draw.rect(screen,"red",(700,100,250,10))
    pygame.draw.rect(screen,"green",(700,100,250*hp_ratio,10))

def bullet_bullet_collision(i):
    d=math.sqrt((alien_bullet_x[i]-bullet_x)**2+(alien_bullet_y[i]-bullet_y)**2)
    if d<=60:
        return True
    else:
        return False
h1=pygame.image.load(path.join(img_dir,"help1.png")).convert_alpha()   
h2=pygame.image.load(path.join(img_dir,"help2.png")).convert_alpha() 
h3=pygame.image.load(path.join(img_dir,"help3.png")).convert_alpha() 
h4=pygame.image.load(path.join(img_dir,"help4.png")).convert_alpha() 
help1=pygame.transform.scale(h1,(screen_width,screen_height))
help2=pygame.transform.scale(h2,(screen_width,screen_height))
help3=pygame.transform.scale(h3,(screen_width,screen_height))
help4=pygame.transform.scale(h4,(screen_width,screen_height))
j=1
help_cool1=True
help_cool2=False
help_cool3=False


asteroid_destroyed=0
alien_killed=0
commander_killed=0
bullets_shot=0
packets_taken=0
hearts_lost=0   

 
img=pygame.image.load(path.join(img_dir,"bg_main.png")).convert_alpha()
main_img=pygame.transform.scale(img,(screen_width,screen_height))
commander=False
loading=True
main_screen=False
asteroid_escape=False
alien_battle=False
help_board=False
crash=False
s_board=False

pygame.mixer.music.load(path.join(sound_folder,"bg.mp3"))
pygame.mixer.music.set_volume(0.2)


run=True
while run:
    
    if loading:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_q:
                   run=False
        m=loading_screen(random.randint(50,70))
        if m:
            main_screen=True
    
    if crash:
        screen.blit(crash_img,(0,0))
        pygame.mixer.music.stop()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    run=False
                if event.key==pygame.K_RETURN:
                    s_board=True
                    crash=False
        
        
    if main_screen:
        screen.blit(main_img,(0,0))
        heart_down=False
        restart()
          
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    run=False
                if event.key==pygame.K_1:
                    main_screen=False
                    asteroid_escape=True
                    alien_battle=False
                    help_board=False
                                    
                if event.key==pygame.K_2:
                      main_screen=False
                      asteroid_escape=False
                      alien_battle=True
                      help_board=False
                if event.key==pygame.K_s:
                       help_board=True
                       main_screen=False
                if event.key==pygame.K_h:
                    s_board=True
                    main_screen=False
    if s_board:
        pygame.mixer.music.stop()
        score_board()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    run=False
                if event.key==pygame.K_RETURN:
                    s_board=False
                    main_screen=True
                    restart()
                       
    if help_board:
        pygame.mixer.music.stop()
        if j==1:
            screen.blit(help1,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    run=False
                if event.key==pygame.K_1:
                       screen.blit(help2,(0,0))
                       j=2
                if event.key==pygame.K_2: 
                       screen.blit(help3,(0,0))
                      
                if event.key==pygame.K_3:
                       screen.blit(help4,(0,0))
                       
                if event.key==pygame.K_RETURN:
                    main_screen=True
                    help_board=False
                    j=1
           
           
           
    if asteroid_escape:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    asteroid_escape=False
                    main_screen=True
        screen.blit(bg,(s,0)) 
        screen.blit(bg,(screen_width+s,0))
        if s ==-screen_width:
            screen.blit(bg,(screen_width+s,0))
            s=0
        s-=1
        hearts()
        
#one heart sound
        if one_heart:
            if n==4:
                one_heartSound.play()
                one_heart=False
        else:
            if n!=4:
                one_heart=True
#shield timming
        if no_shield:
            b+=0.01
            if b==0.9900000000000007:
                shield_time-=1
                b=0
            if shield_time==0:
                no_shield=False
            
#bullet timming
        if no_bullet:
            c+=0.01
            if c==0.9900000000000007:
                bullet_time-=1
                c=0
            if bullet_time==0:
                no_bullet=False
            
#heart timming
        if no_heart:
            d+=0.01
            if d==0.9900000000000007:
                heart_time-=1
                d=0
            if heart_time==0:
                no_heart=False
            
 #shield forming timming 
        if noshield:         
            e+=0.01
            if e==0.9900000000000007:
                 noshield_time-=1
                 e=0
            if noshield_time==0:
                 noshield=False       
    
    #heart down time
        if heart_down:
            z+=0.01
            if z==(0.9900000000000007):
                heart_down=False
                z=0
            
    
    
    #bullets
        if bullet_state=="load":
            bullet_position(player_x, player_y)
            screen.blit(bullet_img,(bullet_x,bullet_y))  
            bullet_y=player_y
            bullet_x=player_x
        time1=pygame.time.get_ticks()
        if not no_shield  :
            screen.blit(player,(player_x,player_y))
        elif no_shield:
            screen.blit(player_shield,(player_x,player_y))
       
        
        cooldown=100      
    #movement of player and boundaries 
        keys=pygame.key.get_pressed()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                if pause:
                    pause=False
                else:
                    pause=True
        if keys[pygame.K_UP] and player_y>=0 and not pause:
            player_y-=player_y_change        
        if keys[pygame.K_DOWN] and player_y<=586 and not pause:
            player_y+=player_y_change
        if keys[pygame.K_RIGHT] and player_x<=936 and not pause:
            player_x+=player_x_change
        if keys[pygame.K_LEFT] and player_x>=0 and not pause:
            player_x-=player_x_change
        if keys[pygame.K_SPACE] and time1-last_shot>cooldown and bullets>0 and not pause :
            bullets-=1
            if bullet_state=="load":
                bullet_x=player_x
                bullet_y=player_y
                bullet_fired()
                bulletSound.play()
                bullets_shot+=1
    
    #asteroids
        if not pause:
            if creating_asteroids:
                for i in range(number_of_asteroids):
                       create_asteroid(asteroid_x[i], asteroid_y[i],i) 
                       asteroid_x[i]-=asteroid_change[i]
                       asteroid_scale[i]=random.uniform(0,2)
                       
                       
                       if asteroid_x[i]<-100:
                           asteroid_x[i]=random.randint(1000,1100)
                           asteroid_y[i]=random.randint(0,650)
               
        #collision
            if creating_asteroids:
                if shield_time<=0:
                    for i in range(number_of_asteroids):
                            collide=asteroid_collision(player_x,player_y,asteroid_x[i],asteroid_y[i])
                            if collide  and not heart_down:
                                 n+=1
                                 hearts_lost+=1
                                 score-=10
                                 hearts()
                                 heart_down=True
                                 if n!=4:
                                     crashSound.play()
                             
                            else:
                                 pass
                elif shield_time>0:
                    for i in range(number_of_asteroids):
                            collide=asteroid_collision(player_x,player_y,asteroid_x[i],asteroid_y[i])
                            if collide:
                                 score+=10
                
            
        #bullet movement
        
            if bullet_state=="fire":
                bullet_fired()
                bullet_x+=bullet_change_x
            if bullet_x>0 and bullet_x>screen_width:
                bullet_state="load"
                bullet_position(player_x, player_y)
    
        #asteroid    
            if creating_asteroids:
                for i in range(number_of_asteroids):  
                    is_collision=bullet_collision(bullet_x,bullet_y,asteroid_x[i],asteroid_y[i])           
                    if is_collision :
                        score+=10
                        asteroid_destroyed+=1
                        x=player_x
                        y=player_y
                        bullet_state="load"
                        hitSound.play()
                        asteroid_x[i]=random.randint(1500,1600)
                        asteroid_y[i]=random.randint(0,650)

        #bullets number
            bullet_number(bullets)  
            display_bullets(f_x,f_y)      
        
        #packets
            if creating_packets:
                if not no_bullet or packet_x<-10:
                    create_packet()
                packet_x-=packet_x_change
                p=packet_collision(player_x,player_y,packet_x,packet_y)
                if p:
                    packets_taken+=1
                    no_bullet=True
                    bullet_time=random.randint(5,10)
                    packetSound.play()
                    bullets+=10
                    packet_x=random.randint(1,1900)
                    packet_y=(random.randint(100,600))
                    packet_x_change=(random.uniform(1,2))
                if packet_x<-10:
                        packet_x=random.randint(1800,1900)
                        packet_y=(random.randint(100,600))
                        packet_x_change=(random.uniform(1,2))
                if not no_heart or packet_x2<-10:
                    create_packet2()
                packet_x2-=packet_x_change2
                p2=packet_collision(player_x,player_y,packet_x2,packet_y2)
                if p2:
                    packets_taken+=1
                    no_heart=True
                    heart_time=random.randint(8,10)
                    packetSound.play()
                    packet_x2=random.randint(1100,1200)
                    packet_y2=(random.randint(100,600))
                    packet_x_change2=(random.uniform(0,1))
                    if n>0:
                        n-=1
                if packet_x2<-10:
                        packet_x2=random.randint(1100,1200)
                        packet_y2=(random.randint(100,600))
                        packet_x_change2=(random.uniform(0,1))
                if not noshield or packet_x<-10:
                    create_packet3()
                packet_x3-=packet_x_change3
                p3=packet_collision(player_x,player_y,packet_x3,packet_y3)
                if p3:
                        packets_taken+=1
                        noshield=True
                        noshield_time=random.randint(5,8)
                        no_shield=True
                        shield_time=5
                        packetSound.play()
                        packet_x3=random.randint(1100,1200)
                        packet_y3=(random.randint(100,600))
                        packet_x_change3=(random.uniform(0,1))
                    
                        if packet_x3<-10:
                            packet_x3=random.randint(1100,1200)
                            packet_y3=(random.randint(100,600))
                            packet_x_change3=(random.uniform(0,1))
                        
            
        #score
            display_score(font_x,font_y)
             
    if alien_battle:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    alien_battle=False
                    main_screen=True
        screen.blit(bg,(s,0)) 
        screen.blit(bg,(screen_width+s,0))
        if s ==-screen_width:
            screen.blit(bg,(screen_width+s,0))
            s=0
        s-=1
        hearts()
        
#one heart sound
        if one_heart:
            if n==4:
                one_heartSound.play()
                one_heart=False
        else:
            if n!=4:
                one_heart=True
#shield timming
        if no_shield:
            b+=0.01
            if b==0.9900000000000007:
                shield_time-=1
                b=0
            if shield_time==0:
                no_shield=False
            
#bullet timming
        if no_bullet:
            c+=0.01
            if c==0.9900000000000007:
                bullet_time-=1
                c=0
            if bullet_time==0:
                no_bullet=False
            
#heart timming
        if no_heart:
            d+=0.01
            if d==0.9900000000000007:
                heart_time-=1
                d=0
            if heart_time==0:
                no_heart=False
            
 #shield forming timming 
        if noshield:         
            e+=0.01
            if e==0.9900000000000007:
                 noshield_time-=1
                 e=0
            if noshield_time==0:
                 noshield=False
        
        if heart_down:
            z+=0.01
            if z==(0.9900000000000007):
                heart_down=False
                z=0
            
    #bullets
        if bullet_state=="load":
            bullet_position(player_x, player_y)
            screen.blit(bullet_img,(bullet_x,bullet_y))  
            bullet_y=player_y
            bullet_x=player_x
        time=pygame.time.get_ticks()
        if not no_shield  :
            screen.blit(player,(player_x,player_y))
        elif no_shield:
            screen.blit(player_shield,(player_x,player_y))
       
        
        cooldown=100      
    #movement of player and boundaries 
        keys=pygame.key.get_pressed()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                if pause:
                    pause=False
                else:
                    pause=True
        if keys[pygame.K_UP] and player_y>=0 and not pause:
            player_y-=player_y_change        
        if keys[pygame.K_DOWN] and player_y<=586 and not pause:
            player_y+=player_y_change
        if keys[pygame.K_RIGHT] and player_x<=936 and not pause:
            player_x+=player_x_change
        if keys[pygame.K_LEFT] and player_x>=0 and not pause:
            player_x-=player_x_change
        if keys[pygame.K_SPACE] and time-last_shot>cooldown and bullets>0 and not pause :
            bullets-=1
            if bullet_state=="load":
                bullet_x=player_x
                bullet_y=player_y
                bullet_fired()
                bulletSound.play()
                bullets_shot+=1

        if bullet_state=="fire":
                bullet_fired()
                bullet_x+=bullet_change_x
        if bullet_x>0 and bullet_x>screen_width:
                bullet_state="load"
                bullet_position(player_x, player_y)
        bullet_number(bullets)  
        display_bullets(f_x,f_y)      
        
        if not pause:
            #packets
            if creating_packets:
                    if not no_bullet or packet_x<-10:
                        create_packet()
                    packet_x-=packet_x_change
                    p=packet_collision(player_x,player_y,packet_x,packet_y)
                    if p:
                        packets_taken+=1
                        no_bullet=True
                        bullet_time=random.randint(5,8)
                        packetSound.play()
                        bullets+=10
                        packet_x=random.randint(1,1900)
                        packet_y=(random.randint(100,600))
                        packet_x_change=(random.uniform(1,2))
                    if packet_x<-10:
                            packet_x=random.randint(1800,1900)
                            packet_y=(random.randint(100,600))
                            packet_x_change=(random.uniform(1,2))
                    if not no_heart or packet_x2<-10:
                        create_packet2()
                    packet_x2-=packet_x_change2
                    p2=packet_collision(player_x,player_y,packet_x2,packet_y2)
                    if p2:
                        packets_taken+=1
                        no_heart=True
                        heart_time=random.randint(8,10)
                        packetSound.play()
                        packet_x2=random.randint(1100,1200)
                        packet_y2=(random.randint(100,600))
                        packet_x_change2=(random.uniform(0,1))
                        if n>0:
                            n-=1
                    if packet_x2<-10:
                            packet_x2=random.randint(1100,1200)
                            packet_y2=(random.randint(100,600))
                            packet_x_change2=(random.uniform(0,1))
                    if not noshield or packet_x<-10:
                        create_packet3()
                    packet_x3-=packet_x_change3
                    p3=packet_collision(player_x,player_y,packet_x3,packet_y3)
                    if p3:
                            packets_taken+=1
                            noshield=True
                            noshield_time=random.randint(5,10)
                            no_shield=True
                            shield_time=5
                            packetSound.play()
                            packet_x3=random.randint(1100,1200)
                            packet_y3=(random.randint(100,600))
                            packet_x_change3=(random.uniform(0,1))
                        
                            if packet_x3<-10:
                                packet_x3=random.randint(1100,1200)
                                packet_y3=(random.randint(100,600))
                                packet_x_change3=(random.uniform(0,1))
                                
                   
                    if not commander:                             
                        for i in range(number_of_aliens):
                                       create_alien(alien_x[i], alien_y[i],i) 
                                       alien_x[i]-=alien_change[i]
                                      
                                       if alien_x[i]<-100:
                                           alien_x[i]=random.randint(1000,1100)
                                           alien_y[i]=random.randint(0,650)
                               
                        if shield_time<=0:
                            for i in range(number_of_aliens):
                                            collide=alien_collision(player_x,player_y,alien_x[i],alien_y[i])
                                            if collide and not heart_down:
                                                 score-=10
                                                 n+=1
                                                 hearts_lost+=1
                                                 hearts()
                                                 heart_down=True
                                                 if n!=4:
                                                     crashSound.play()
                                             
                                            else:
                                                 pass
                        elif shield_time>0:
                                    for i in range(number_of_aliens):
                                            collide=alien_collision(player_x,player_y,alien_x[i],alien_y[i])
                                            if collide:
                                                pass
                                
                        for i in range(number_of_aliens):  
                                         is_collision=bullet_collision(bullet_x,bullet_y,alien_x[i],alien_y[i])           
                                         if is_collision :
                                             alien_killed+=1
                                             score+=10
                                             x=player_x
                                             y=player_y
                                             bullet_state="load"
                                             hitSound.play()
                                             alien_x[i]=random.randint(1500,1600)
                                             alien_y[i]=random.randint(0,650)
                        
                        for i in range(number_of_aliens):
                            if alien_bullet_state[i]=="load":
                                      alien_bullet_x[i]=alien_x[i]
                                      alien_bullet_y[i]=alien_y[i]
                            
                        for i in range(number_of_aliens):
                            if alien_y[i]==player_y:
                                alien_bullet_state[i]="fire"
                             
                            if alien_bullet_state[i]=="fire":
                                   alien_bullet_fired(i)
                                   alien_bullet_x[i]-=alien_bullet_change_x[i]
                    
                            if alien_bullet_x[i]<0 and alien_bullet_x[i]<screen_width:
                                  alien_bullet_state[i]="load"
                                  alien_bullet_position(alien_x[i],alien_y[i],i)         
                       
                        for i in range(number_of_aliens):
                            alien_bullet_collide=alien_bullet_collision(player_x,player_y,alien_bullet_x[i],alien_bullet_y[i])
                            bullet_bullet_collide=bullet_bullet_collision(i)
                            if not noshield:
                                    if alien_bullet_collide and not heart_down:
                                       x=alien_x[i]
                                       y=alien_y[i]
                                       alien_bullet_state[i]="load"
                                       score-=10
                                       score+=10
                                       n+=1
                                       hearts_lost+=1
                                       crashSound.play()
                                    else:
                                        pass
                            elif noshield:
                                    if alien_bullet_collide:
                                        x=alien_x[i]
                                        y=alien_y[i]
                                        alien_bullet_state[i]="load"
                                        hitSound.play()
                            if bullet_bullet_collide:
                                alien_bullet_x[i]=-100
                                alien_bullet_y[i]=-100
                                bullet_x=player_x
                                bullet_y=player_y
                                bullet_state="load"
                                hitSound.play()
                                
                            
                    if score%200==0 and score>0 and score%2200!=0:
                           commander=True
                           create_commmander()
                           commander_x-=0.5
                           if commander_x<750:
                               commander_x=750
                               
                           if commander_x==750:
                               
                               if player_y>commander_y+40 and commander_y<=450:
                                  commander_y+=1
                               elif player_y<commander_y+40:
                                       commander_y-=1
                           
                               if commander_rocket_state=="load":
                                             commander_rocket_x=commander_x
                                             commander_rocket_y=commander_y
                                   
                            
                               if commander_y+40==player_y  :
                                       commander_rocket_state="fire"
                                    
                               if commander_rocket_state=="fire":
                                          commander_rocket_fired()
                                          commander_rocket_x-=commander_rocket_change_x
                           
                               if commander_rocket_x<0 and commander_rocket_x<screen_width:
                                         commander_rocket_state="load"
                                         commander_rocket_position(commander_x,commander_y)         
                              
                               commander_rocket_collide=commander_rocket_collision(player_x,player_y+27,commander_rocket_x,commander_rocket_y)
                               commander_rocket_collide1=commander_rocket_collision(player_x,player_y-27,commander_rocket_x,commander_rocket_y)
                               commander_rocket_collide2=commander_rocket_collision(player_x,player_y,commander_rocket_x,commander_rocket_y)
                               
                               
                               bullet_rocket_collide=bullet_rocket_collision()
                               if not noshield:
                                   if commander_rocket_collide or commander_rocket_collide1 or commander_rocket_collide2:
                                              x=commander_rocket_x
                                              y=commander_rocket_y
                                              commander_rocket_state="load"
                                              n+=1
                                              crashSound.play()
                                              if n==5:
                                                  
                                                  game_over()
                                   else:    
                                               pass
                               elif noshield:
                                           if commander_rocket_collide:
                                               x=commander_rocket_x
                                               y=commander_rocket_y
                                               commander_rocket_state="load"
                                               hitSound.play()
                               if bullet_rocket_collide:
                                      
                                           commander_rocket_x=-100
                                           commander_rocket_y=-100
                                           bullet_x=player_x
                                           bullet_y=player_y
                                           bullet_state="load"
                                           hitSound.play()
                               player_commander_collide=player_commander_collision(player_x,player_y,commander_x,commander_y+100)
                               player_commander_collide1=player_commander_collision(player_x,player_y,commander_x,commander_y)
                               player_commander_collide2=player_commander_collision(player_x,player_y,commander_x,commander_y+35)
                                                                                   
                               if player_commander_collide or player_commander_collide1:
                                  player_x=0
                                  n+=1
                               
                               if player_y<80 or player_y>525:
                                   player_y=300
                                  
                               if player_commander_collide2:
                                   player_x=0
                                   n+=1
                                   crashSound.play()
                                   
                               commander_bullet_collide=commander_bullet_collision(bullet_x,bullet_y,commander_x,commander_y+35)
                               commander_bullet_collide1=commander_bullet_collision(bullet_x,bullet_y,commander_x,commander_y+100)
                               commander_bullet_collide2=commander_bullet_collision(bullet_x,bullet_y,commander_x,commander_y)
                               if not commander_bullet_collide:
                                   commander_health_draw()
                               
                               if commander_bullet_collide or commander_bullet_collide1 or commander_bullet_collide1 and bullet_rocket_collide:
                                   x=player_x
                                   y=player_y
                                   bullet_state="load"
                                   hitSound.play()
                                   hp-=10
                            
                            
                               if hp==0:
                                    commander_killed+=1
                                    real_score=score
                                    real_n=n
                                    real_bullets=bullets
                                
                                    restart()
                                    commander=False
                                    score=real_score+2000
                                    n=real_n
                                    bullets=real_bullets
                                    
                                   
                                 
                    
            #score
            display_score(font_x,font_y)
    pygame.display.flip()

pygame.quit()        