# напиши свой код здесь
key_switch_camera = 'c'
key_switch_noclip = 'z'

key_move_forward = 'w'
key_move_left = 'a'
key_move_backward = 's'
key_move_right = 'd'
key_move_up = 'e'
key_move_down = 'q'

key_turn_left = 'j'
key_turn_right = 'l'
key_turn_up = 'i'
key_turn_down = 'k'

key_build = 'b'
key_destroy = 'n'


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.noclip = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setHpr(180, 0, 0)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
    
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    
    def changeMode(self):
        if self.noclip:
            self.noclip = False
        else:
            self.noclip =True

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5)%360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5)%360)

    def turn_up(self):
        if self.hero.getP() >= -80:
            self.hero.setP(self.hero.getP() - 5)

    def turn_down(self):
        if  self.hero.getP() <= 80:
            self.hero.setP(self.hero.getP() + 5)

    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        x_to = dx + x_from
        y_to = dy + y_from
        z_to = z_from

        return x_to, y_to, z_to

    def check_dir(self, angle):
        if angle >=0 and angle<=20:
            return(0,-1)
        if angle<=65:
            return(1,-1)
        if angle<=110:
            return(1,0)
        if angle<=155:
            return(1,1)
        if angle<=200:
            return(0,1)
        if angle<=245:
            return(-1,1)
        if angle<=290:
            return(-1,0)
        if angle<=335:
            return(-1,-1)
        else:
            return(0,-1)

    def check_vert(self,angle):
        if angle > 30:
            return(-1)
        if angle <= 30 and angle > -30:
            return(0)
        if angle <= -30: 
            return(1)

    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)
    
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def backward(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    
    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)


    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if (not self.land.isEmpty((pos[0], pos[1], pos[2] - 1))) and self.land.isEmpty(pos):
            self.hero.setPos(pos)
        elif not self.land.isEmpty(pos):
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
        else:
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
            

    def move_to(self, angle):
        if self.noclip:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        print(self.check_vert(self.hero.getP()))
        pos = pos[0], pos[1], pos[2] + self.check_vert(self.hero.getP())
        self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        pos = pos[0], pos[1], pos[2] + self.check_vert(self.hero.getP())
        self.land.delBlockFrom(pos)



    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)
        base.accept(key_turn_up, self.turn_up)
        base.accept(key_turn_up + '-repeat', self.turn_up)
        base.accept(key_turn_down, self.turn_down)
        base.accept(key_turn_down + '-repeat', self.turn_down)

        base.accept(key_move_forward, self.forward)
        base.accept(key_move_forward + '-repeat', self.forward)
        base.accept(key_move_backward, self.backward)
        base.accept(key_move_backward + '-repeat', self.backward)
        base.accept(key_move_left, self.left)
        base.accept(key_move_left + '-repeat', self.left)
        base.accept(key_move_right, self.right)
        base.accept(key_move_right + '-repeat', self.right)
        base.accept(key_move_up, self.up)
        base.accept(key_move_up + '-repeat', self.up)
        base.accept(key_move_down, self.down)
        base.accept(key_move_down + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_noclip, self.changeMode)