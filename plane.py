import pygame

class plane(object):
    def __init__(self,image,blood) -> None:
        self.image=image
        self.blood=blood
    
    def shoot(self,bullet):
        pass

    def is_shot(self):
        for my_bullet in my_bullets:
            pass
    

class my_plane(plane):
    pass

class enemy_plane(plane):
    def __init__(self, image, blood,type) -> None:
        super().__init__(image, blood)
        self.type=type
        if self.type==0:
            self.blood=1
        elif self.type==1:
            self.blood=4
        elif self.type==2:
            self.blood=10
    
    def destroy(self):
        if self.type==0:
            if self.blood==0:
                enemy_plane01=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy0_down1.png')
                enemy_plane02=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy0_down2.png')
                enemy_plane03=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy0_down3.png')
                enemy_plane04=pygame.image.load(r'70a3277d31b84c6a907848c6682dd55b\feiji\enemy0_down4.png')
                


class maingame(object):
