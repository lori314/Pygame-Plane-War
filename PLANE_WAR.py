import pygame
import sys
import random








class hero_plane(pygame.sprite.Sprite):
    def __init__(self,enemy,enemy_bullets,things,scr) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\hero1.png')
        self.rect=self.image.get_rect()
        self.rect.topleft=(0,0)
        self.blood=100
        self.bullets=pygame.sprite.Group()
        self.count=0
        self.enemy=enemy
        self.enemy_bullets=enemy_bullets
        self.bomb=Bomb(-1,scr)
        self.live=True
        self.scr=scr
        self.things=things
        self.double=False
    
    def display(self):
        self.scr.blit(self.image,self.rect)

    def move(self):
        mouse_pos=pygame.mouse.get_pos()
        if mouse_pos[0]>=0 and mouse_pos[0]<=480 and mouse_pos[1]>=0 and mouse_pos[1]<=852:
            self.rect.x=mouse_pos[0]-self.rect.width/2
            self.rect.y=mouse_pos[1]-self.rect.height/2
    
    def shoot(self):
        self.count+=1
        if self.count%10==0:
            my_bullet=bullet(0,self.rect.x,self.rect.y,self.scr)
            self.bullets.add(my_bullet)     
        if self.count>=10000:
            self.count=0
        for my_bullet in self.bullets:
            my_bullet.automove()
            my_bullet.display()
    
    def isdestroyed(self):
        if not pygame.sprite.spritecollide(self,self.enemy,True)==[]:
            self.bomb.action(self.rect)
            self.blood-=5
            if self.blood<=0:
                self.live=False
            self.double=False
            self.bomb.draw()
        if not pygame.sprite.spritecollide(self,self.enemy_bullets,True)==[]:
            self.bomb.action(self.rect)
            self.blood-=2
            if self.blood<=0:
                self.live=False
            self.double=False
            self.bomb.draw()
        thing_list=pygame.sprite.spritecollide(self,self.things,True)
        if thing_list !=[]:
            for thing in thing_list:
                if thing.type==1:
                    if self.double==False:
                        self.double=True
                elif thing.type==2:
                    for enemy in self.enemy:
                        enemy.blood=0
            
        if self.double==True:
            if self.count%3==0:
                my_bullet=bullet(0,self.rect.x,self.rect.y,self.scr)
                self.bullets.add(my_bullet)     
            if self.count>=10000:
                self.count=0
        

class enemy_plane(pygame.sprite.Sprite):
    def __init__(self,type,scr) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=type
        if type=='small':
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy0.png')
            self.speed=random.randint(6,8)
            self.blood=1
            self.bomb=Bomb(0,scr)
            self.score=1
        elif type=='middle':
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy1.png')
            self.speed=4
            self.blood=4
            self.bomb=Bomb(1,scr)
            self.score=4
        elif type=='big':
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy2.png')
            self.speed=2
            self.blood=10
            self.bomb=Bomb(2,scr)
            self.score=10
        self.rect=self.image.get_rect()
        x=random.randint(0,480-self.rect.width)
        self.rect.topleft=(x,0)
        self.count=0
        self.bullets=pygame.sprite.Group()
        self.live=True
        self.back=False
        self.scr=scr

    def auto_move(self):
        self.rect.y+=self.speed
        
    def display(self):
        self.scr.blit(self.image,self.rect)  
    
    def shoot(self):
        self.count+=1
        if self.count%100==0:
            if self.type=='big':
                my_bullet=bullet(2,self.rect.x,self.rect.y,self.scr)
                self.bullets.add(my_bullet)   
            if self.type=='middle':
                my_bullet=bullet(1,self.rect.x,self.rect.y,self.scr)  
                self.bullets.add(my_bullet) 
        if self.count>=10000:
            self.count=0
        for my_bullet in self.bullets:
            my_bullet.automove()
            my_bullet.display()
    
    def isdestroyed(self,player_bullets):
        global score
        if not pygame.sprite.spritecollide(self,player_bullets,True)==[]:
            self.bomb.action(self.rect)
            self.blood-=1
            self.rect.y-=5
        if self.blood<=0:
            self.bomb.action(self.rect)
            self.live=False
        self.bomb.draw()
        if self.live==False and self.bomb.visible==False:
            score+=self.score
            self.back=True
        elif self.live==False and self.bomb.visible==True:
            self.rect.y-=self.speed
        
    

class bullet(pygame.sprite.Sprite):
    def __init__(self,type,x,y,scr) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=type
        if type==0:
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\bullet.png')
            self.rect=self.image.get_rect()
            self.rect.topleft=(x+50-11,y)
            self.speed=40
        if type==1:
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\bullet1.png')
            self.rect=self.image.get_rect()
            self.rect.topleft=(x+68/2-8/2,y+89)
            self.speed=5
        if type==2:
            self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\bullet2.png')
            self.rect=self.image.get_rect()
            self.rect.topleft=(x+164/2-8/2,y+246)
            self.speed=3
        self.scr=scr
        
    def automove(self):
        if self.type==0:
            self.rect.y-=self.speed

        else:
            self.rect.y+=self.speed
    
    def display(self):
        self.scr.blit(self.image,self.rect)
            
class Bomb(pygame.sprite.Sprite):
    def __init__(self,type,scr) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=type
        if type==-1:
            self.image=[pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\hero_blowup_n'+str(v)+'.png') for v in range(1,5)]
        elif type==0 or type==1:
            self.image=[pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy'+str(self.type)+'_down'+str(v)+'.png') for v in range(1,5)]
        else:
            self.image=[pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy'+str(self.type)+'_down'+str(v)+'.png') for v in range(1,7)]
        self.index=0
        self.visible=False
        self.pos=[0,0]
        self.count=0
        self.scr=scr

    def action(self,rect):
        self.pos[0]=rect.x
        self.pos[1]=rect.y
        self.visible=True
    
    def draw(self):
        if self.visible == False:
            return
        self.scr.blit(self.image[self.index],(self.pos[0],self.pos[1]))
        self.count+=1
        if self.type==0:
            if self.count%2==0:
                self.index+=1
        else:
            if self.count%5==0:
                self.index+=1
        if self.index>=len(self.image):
            self.visible=False
            self.index=0
            self.count=0

class thing(pygame.sprite.Sprite):
    def __init__(self,scr) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type=random.randint(1,2)
        self.image=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\bomb-'+str(self.type)+'.gif')
        self.speed=3
        self.rect=self.image.get_rect()
        x=random.randint(0,470)
        self.rect.topleft=(x,0)
        self.scr=scr
    
    def auto_move(self):
        self.rect.y+=self.speed
    
    def display(self):
        self.scr.blit(self.image,self.rect)


class number(object):
    def __init__(self,num,scr) -> None:
        self.value=num
        self.images=[pygame.image.load('70a3277d31b84c6a907848c6682dd55b\\feiji\\'+str(v)+'.jpg') for v in range(0,10)]
        self.rect=pygame.Rect(350,0,28,39)
        self.scr=scr
    def display(self):
        if self.value>=1000:
            self.value-=1000
        if self.value>=0 and self.value<=9:
            self.scr.blit(self.images[self.value],self.rect)
        elif self.value>=10 and self.value<=99:
            x=self.value%10
            y=self.value//10
            self.scr.blit(self.images[y],(320,0,28,39))
            self.scr.blit(self.images[x],(350,0,28,39))
        elif self.value>=100:
            x=self.value%10
            y=((self.value-x)//10)%10
            z=self.value//100
            self.scr.blit(self.images[z],(290,0,28,39))
            self.scr.blit(self.images[y],(320,0,28,39))
            self.scr.blit(self.images[x],(350,0,28,39))
    def get_value(self,value):
        self.value=value

class life(object):
    def __init__(self,num,scr) -> None:
        self.value=num
        self.images=[pygame.image.load('70a3277d31b84c6a907848c6682dd55b\\feiji\\'+str(v)+'.jpg') for v in range(0,10)]
        self.rect=pygame.Rect(160,0,28,39)
        self.scr=scr
    def display(self):
        if self.value>=0 and self.value<=9:
            self.scr.blit(self.images[self.value],self.rect)
        elif self.value>=10 and self.value<=99:
            x=self.value%10
            y=self.value//10
            self.scr.blit(self.images[y],(130,0,28,39))
            self.scr.blit(self.images[x],(160,0,28,39))
        elif self.value>=100:
            x=self.value%10
            y=((self.value-x)//10)%10
            z=self.value//100
            self.scr.blit(self.images[z],(100,0,28,39))
            self.scr.blit(self.images[y],(130,0,28,39))
            self.scr.blit(self.images[x],(160,0,28,39))
    def get_value(self,value):
        self.value=value

class Maneger(object):
    def __init__(self,scr) -> None:
        self.scr=scr
    def main(self):
        global status
        background=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\background.png')
        background_rect=(0,0,480,852)
        enemy_planes=pygame.sprite.Group()
        enemy_plane_bullets=pygame.sprite.Group()
        things=pygame.sprite.Group()
        player=hero_plane(enemy_planes,enemy_plane_bullets,things,self.scr)
        clock=pygame.time.Clock()
        count=0
        global best_score
        global score
        score=0
        board=number(score,self.scr)
        life_board=life(player.blood,self.scr)
        while True:
            clock.tick(60)
            count+=1
            if count>=10000:
                count=0
            self.scr.blit(background,background_rect)
            if player.live==False:
                status=2
                if score>best_score:
                    best_score=score
                break
            player.move()
            player.display()
            player.shoot()
            player.isdestroyed()
            for bullet in player.bullets:
                if bullet.rect.y<=0:
                    player.bullets.remove(bullet)
            if count%20==0:
                i=random.randint(0,10)
                if i==0:
                    enemy=enemy_plane('big',self.scr)
                elif i>=1 and i<=3:
                    enemy=enemy_plane('middle',self.scr)
                else:
                    enemy=enemy_plane('small',self.scr)
                enemy_planes.add(enemy)
            if count%200==0:
                my_thing=thing(self.scr)
                things.add(my_thing)
            for enemy in enemy_planes:
                enemy.auto_move()
                if enemy.rect.y>=852:
                    enemy_planes.remove(enemy)
                enemy.shoot()
                for bullet in enemy.bullets:
                    if bullet.rect.y>=852:
                        enemy.bullets.remove(bullet)
                        enemy_plane_bullets.remove(bullet)
                    enemy_plane_bullets.add(bullet)
                enemy.isdestroyed(player.bullets)
                enemy.display()
                if enemy.back==True:
                    enemy_planes.remove(enemy)
            for my_thing in things:
                my_thing.auto_move()
                if my_thing.rect.y>=852:
                    things.remove(my_thing)
                my_thing.display()
            board.get_value(score)
            board.display()
            life_board.get_value(player.blood)
            life_board.display()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
    
    def start(self):
        global status
        background=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\background.png')
        background_rect=(0,0,480,852)
        title=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\name.png')
        title_rect=(25,50,429,84)
        start_btn=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\game_resume_pressed.png')
        start_btn_rect=pygame.Rect(220,500,38,41)
        plane=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\hero.gif')
        plane_rect=(190,200,100,124)
        clock=pygame.time.Clock()
        while True:
            clock.tick(60)
            self.scr.blit(background,background_rect)
            self.scr.blit(title,title_rect)
            self.scr.blit(start_btn,start_btn_rect)
            self.scr.blit(plane,plane_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if event.pos[0]>=start_btn_rect.x and event.pos[0]<=start_btn_rect.x+start_btn_rect.width and event.pos[1]>=start_btn_rect.y and event.pos[1]<=start_btn_rect.y+start_btn_rect.height:
                        status=1
            if status==1:
                break

    def game_over(self):
        global status
        background=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\gameover.png')
        background_rect=(0,0,480,852)
        images=[pygame.image.load('70a3277d31b84c6a907848c6682dd55b\\feiji\\'+str(v)+'.jpg') for v in range(0,10)]
        re_start=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\restart_sel.png')
        re_start_rect=pygame.Rect(185,700,110,24)
        give_up=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\quit_sel.png')
        give_up_rect=pygame.Rect(185,750,110,24)
        while True:
            self.scr.blit(background,background_rect)
            if score>=0 and score<=9:
                self.scr.blit(images[score],(250,600,28,39))
            elif score>=10 and score<=99:
                x=score%10
                y=score//10
                self.scr.blit(images[y],(220,600,28,39))
                self.scr.blit(images[x],(250,600,28,39))
            elif score>=100:
                x=score%10
                y=((score-x)//10)%10
                z=score//100
                self.scr.blit(images[z],(220,600,28,39))
                self.scr.blit(images[y],(250,600,28,39))
                self.scr.blit(images[x],(280,600,28,39))
            
            if best_score>=0 and best_score<=9:
                self.scr.blit(images[best_score],(250,300,28,39))
            elif best_score>=10 and best_score<=99:
                x=best_score%10
                y=best_score//10
                self.scr.blit(images[y],(220,300,28,39))
                self.scr.blit(images[x],(250,300,28,39))
            elif best_score>=100:
                x=best_score%10
                y=((best_score-x)//10)%10
                z=best_score//100
                self.scr.blit(images[z],(220,300,28,39))
                self.scr.blit(images[y],(250,300,28,39))
                self.scr.blit(images[x],(280,300,28,39))
            self.scr.blit(give_up,give_up_rect)
            self.scr.blit(re_start,re_start_rect)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if event.pos[0]>=re_start_rect.x and event.pos[0]<=re_start_rect.x+re_start_rect.width and event.pos[1]>=re_start_rect.y and event.pos[1]<=re_start_rect.y+re_start_rect.height:
                        status=1
                    elif event.pos[0]>=give_up_rect.x and event.pos[0]<=give_up_rect.x+give_up_rect.width and event.pos[1]>=give_up_rect.y and event.pos[1]<=give_up_rect.y+give_up_rect.height:
                        pygame.quit()
                        sys.exit()
            pygame.display.update() 
            if status==1:
                break


        


if __name__=='__main__':    
    pygame.init() 
    scr=pygame.display.set_mode((480,852))
    manager=Maneger(scr)
    score=0
    best_score=0
    status=0
    while True:
        if status==0:
            manager.start()
        elif status==1:
            manager.main()  
        elif status==2:
            manager.game_over() 
    
