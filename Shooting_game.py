import pyxel

SCREEN_WIDTH = 105
SCREEN_HEIGHT = 150
START_SCENE = "start"
PLAY_SCENE = "play"
PHASE_ONE = "phase1"

#プレイヤーのHP 30の倍数に設定
P_HP = 60
#初期スコアのコントロール(初期値0) 5000 → フェーズ2　10000 → フェーズ3
SCORE = [0,0,0,0,0,0,0,0]
T_SCORE = 0
#フェーズ移行するスコアの制御
PHASE2_SCORE = 5000
PHASE3_SCORE = 10000
#プレイヤーのダメージ判定の制御
Damage_switch = True
#敵1のHP　10の倍数に設定
ENEMY1_HP = 70
#ボスのHP 40の倍数に設定
BOSS_HP = 1600



#弾用クラス
class Bullet:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type

    def update(self):
        if self.y > -3:
            self.y -= 5

    def draw(self):
        if self.type==1:
            pyxel.blt(self.x,self.y,0,0,8,1,3)
        elif self.type==2:
            pyxel.blt(self.x,self.y,0,97,2,7,1)

#敵（隕石）用クラス
class Comet:
    def __init__(self,x,y,speed,level):
        self.x = x
        self.y = y
        self.speed = speed
        self.level = level
        self.HP = (level*2-1)*10

    def update(self):
        if self.HP%10==0:
            if self.y <= SCREEN_HEIGHT:
                self.y += self.speed
        else:
            if self.HP>=10:
                if self.y <= SCREEN_HEIGHT:
                    self.y += self.speed/2
                self.HP-=1
            else:
                self.HP-=1

    def draw(self):
        if self.HP%2==0:
            if self.level == 1:
                pyxel.blt(self.x,self.y,0,45,0,6,10,pyxel.COLOR_BLACK)
            elif self.level == 2:
                pyxel.blt(self.x,self.y,0,61,0,7,13,pyxel.COLOR_BLACK)
            elif self.level == 3:
                pyxel.blt(self.x,self.y,0,75,0,10,15,pyxel.COLOR_BLACK)
                
#敵１用クラス
class Enemy1:
    def __init__(self,x,y):
        self.x = x
        self.y = -8
        self.end_y = y
        self.HP = ENEMY1_HP
        self.start_switch = False
        self.start_time = 0

    def update(self):
        if self.y < self.end_y:
            self.y += 1
        else:
            if not self.start_switch:
                self.start_time = pyxel.frame_count
                self.start_switch = True
        
        if self.HP%10!=0:
            self.HP-=1
        
            
    def draw(self):
        if self.HP%2==0:
            if self.y < self.end_y:
                if pyxel.frame_count%20<10:
                    pyxel.blt(self.x,self.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                else:
                    pyxel.blt(self.x,self.y,0,122,16,8,8,pyxel.COLOR_BLACK)
            else:
                if (pyxel.frame_count-self.start_time)%120>=100:
                    if pyxel.frame_count%20<10:
                        pyxel.blt(self.x,self.y,0,24,0,9,9,pyxel.COLOR_BLACK)
                    else:
                        pyxel.blt(self.x,self.y,0,112,16,9,9,pyxel.COLOR_BLACK)
                else:
                    if pyxel.frame_count%20<10:
                        pyxel.blt(self.x,self.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                    else:
                        pyxel.blt(self.x,self.y,0,122,16,8,8,pyxel.COLOR_BLACK)

#敵１の弾丸用クラス
class Enemy1_Fire:
    def __init__(self,x,y,ex,ey):
        self.x = x
        self.y = y
        self.end_x = ex
        self.end_y = ey
        if ex-x>3:
            self.x_speed = abs((ex-x)/((y-ey)/4))
        elif ex-x<-3:
            self.x_speed = -abs((ex-x)/((y-ey)/4))
        else:
            self.x_speed = 0
        self.y_speed = 4

    def update(self):
        if -1<=self.x<=106 and -1<=self.y<=151:
            self.x += self.x_speed
            self.y += self.y_speed

    def draw(self):
        if pyxel.frame_count%4<=1:
            pyxel.blt(self.x,self.y,0,28,11,2,2)
        else:
            pyxel.blt(self.x,self.y,0,31,11,2,2)

#ボス用クラス
class BOSS:
    def __init__(self):
        self.x = SCREEN_WIDTH//2-5
        self.y = 20
        self.start_HP = BOSS_HP
        self.HP = BOSS_HP
        self.start_switch = False
        self.start_frame = 0
        self.start_count = 40
        self.end_count = 50
        self.phase1 = False
        self.phase2 = False
        self.phase3 = False
        self.phase_f = False
        self.Gameover = False
        self.GmTime = 0
        self.NowTime = 0
    
    def update(self):
        if not self.Gameover:
            if not self.start_switch:
                if self.start_count > 0:
                    self.start_count-=1
                else:
                    if not self.start_switch:
                        self.start_switch = True
                        self.start_frame = pyxel.frame_count
                        self.phase1 = True
            
            if self.phase1:
                if self.HP==(self.start_HP//4)*2:
                    self.phase1 = False
                    self.phase2 = True

            if self.phase2:
                if self.HP==self.start_HP//4:
                    self.phase2 = False
                    self.phase3 = True

            if self.phase3:
                if self.HP==0:
                    self.phase3 = False
                    self.phase_f = True

            if self.phase_f:
                if self.end_count > -1:
                    self.end_count-=1

        if self.HP%10!=0:
            self.HP-=1
        
        if self.start_switch:
            if not self.Gameover:
                self.NowTime = pyxel.frame_count-self.start_frame
            else:
                self.NowTime = self.GmTime



    def draw(self):
        if not self.start_switch:
            if 20<self.start_count<=40:
                if self.start_count%2==0:
                    pyxel.blt(self.x,self.y,0,122,33,12,17,pyxel.COLOR_GREEN)
            elif 0<self.start_count<=20:
                if self.start_count%4<2:
                    pyxel.blt(self.x,self.y,0,122,33,12,17,pyxel.COLOR_GREEN)

        else:
            if self.phase1:
                if self.HP%2==0:
                    if self.NowTime%120<100:
                        if self.NowTime%4<2:
                            pyxel.blt(self.x,self.y,0,122,33,12,17,pyxel.COLOR_GREEN)
                        else:
                            pyxel.blt(self.x,self.y,0,122,57,12,17,pyxel.COLOR_GREEN)
                    else:
                        if self.NowTime%4<2:
                            pyxel.blt(self.x,self.y,0,138,33,12,20,pyxel.COLOR_GREEN)
                        else:
                            pyxel.blt(self.x,self.y,0,138,57,12,20,pyxel.COLOR_GREEN)
                else:
                    if self.NowTime%120<100:
                        if self.NowTime%4<2:
                            pyxel.blt(self.x,self.y,0,122,33,12,12,pyxel.COLOR_GREEN)
                        else:
                            pyxel.blt(self.x,self.y,0,122,57,12,12,pyxel.COLOR_GREEN)
                    else:
                        if self.NowTime%4<2:
                            pyxel.blt(self.x,self.y,0,138,33,12,16,pyxel.COLOR_GREEN)
                        else:
                            pyxel.blt(self.x,self.y,0,138,57,12,16,pyxel.COLOR_GREEN)

            elif self.phase2:
                if self.HP%2==0:
                    if self.NowTime%4<2:
                        pyxel.blt(self.x,self.y,0,138,33,12,16,pyxel.COLOR_GREEN)
                    else:
                        pyxel.blt(self.x,self.y,0,138,57,12,16,pyxel.COLOR_GREEN)

            elif self.phase3:
                if self.HP%2==0:
                    if self.NowTime%4<2:
                        pyxel.blt(self.x,self.y,0,154,33,12,16,pyxel.COLOR_GREEN)
                    else:
                        pyxel.blt(self.x,self.y,0,154,57,12,16,pyxel.COLOR_GREEN)

            elif self.phase_f:
                if self.end_count>=0:
                    if self.end_count%2==0:
                        pyxel.blt(self.x,self.y,0,170,33,12,16,pyxel.COLOR_GREEN)

        
class BOSS_fire:
    def __init__(self,x,y,ex,ey):
        self.x = x
        self.y = y
        self.end_x = ex
        self.end_y = ey
        if ex-x>3:
            self.x_speed = abs((ex-x)/((y-ey)/4))
        elif ex-x<-3:
            self.x_speed = -abs((ex-x)/((y-ey)/4))
        else:
            self.x_speed = 0
        self.y_speed = 4
        self.Gameover = False
        self.GmTime = 0
        self.NowTime = 0

    def update(self):
        if not self.Gameover:
            self.NowTime = pyxel.frame_count
            if -1<=self.x<=106 and -1<=self.y<=151:
                self.x += self.x_speed
                self.y += self.y_speed
        else:
            self.NowTime = self.GmTime

    def draw(self):
        if self.NowTime%6<=1:
            pyxel.blt(self.x,self.y,0,123,53,2,2)
        elif 2<=self.NowTime%6<=3:
            pyxel.blt(self.x,self.y,0,126,53,2,2)
        else:
            pyxel.blt(self.x,self.y,0,129,53,2,2)

#ゲーム全体のクラス
class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT,title="シューティングゲーム")
        pyxel.load("my_resource.pyxres")
        
        #データセーブ用##############################################################
        
        import os
        import sys
        
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        self.score_path = os.path.join(base_path, "SAVE_score.txt")
        self.kinds_path = os.path.join(base_path, "SAVE_kinds.txt")
        
        if not os.path.exists(self.score_path):
            with open(self.score_path, "w") as f:
                f.write("0 0 0 0 5 0 0 0")

        if not os.path.exists(self.kinds_path):
            with open(self.kinds_path, "w") as f:
                f.write("1")
                
        ###########################################################################

        self.current_scene = START_SCENE
        self.current_phase = ""
        self.phase_one = False
        self.phase_two = False
        self.phase_three = False
        self.BOSS = 0
        
        self.player_x = SCREEN_WIDTH//2-3
        self.player_y = 130
        self.player_HP = P_HP
        self.player_type = 1
        self.type_number = 0
        self.Player_Change = False
        self.change_scene = 30
        self.player_unlock1 = False

        self.play_interval = 40
        self.start_frame = 0
        self.score = SCORE.copy()
        self.total_score = T_SCORE

        #データのロード######################################################################

        with open(self.kinds_path,"r") as x:
            x = x.read()
            P_list = list(map(int,x.split()))
        self.type_list = P_list

        self.score_ranking = []
        self.first = ["-"]*8
        self.second = ["-"]*8
        self.third = ["-"]*8
        self.fourth = ["-"]*8
        self.fifth = ["-"]*8
        
        with open(self.score_path,"r") as x:
            x = x.readlines()
            for i in range(len(x)):
                self.score_ranking.append(list(map(int,x[i].strip().split())))
                
        self.first = self.score_ranking[0]
        if len(self.score_ranking)>=2:self.second = self.score_ranking[1]
        if len(self.score_ranking)>=3:self.third = self.score_ranking[2]
        if len(self.score_ranking)>=4:self.fourth = self.score_ranking[3]
        if len(self.score_ranking)>=5:self.fifth = self.score_ranking[4]

        ###################################################################################
        
        self.ranking_switch = "off"

        self.Bullets = []
        self.Comets = []
        self.Enemy1R = []
        self.Enemy1R_fire = []
        self.Enemy1L = []
        self.Enemy1L_fire = []
        self.Boss_fire = []
        
        self.comet_interval = 20

        self.start_switch = "off"

        self.Game_start = False
        self.GAME_OVER = False
        self.gameover_time = -1

        pyxel.run(self.update,self.draw)

#アップデート
    def update_boss(self):     #ボス用処理#
        #####################################################################################################################
        if self.BOSS==0:
            self.BOSS = BOSS()
        else:
            if self.GAME_OVER:
                if not self.BOSS.Gameover:
                    self.BOSS.Gameover = True
                    self.BOSS.GmTime = self.gameover_frame
            self.BOSS.update()
            if self.BOSS.phase1:
                if self.BOSS.NowTime%120==105:
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,self.player_x-7,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,self.player_x+3,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,self.player_x+13,self.player_y+5))
                    pyxel.playm(6,loop=False)
            if self.BOSS.phase2:
                if self.BOSS.NowTime%240==105:
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,5,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//4,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//2,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//4*3,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,100,self.player_y+5))
                    pyxel.playm(6,loop=False)
                elif self.BOSS.NowTime%240==225:
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//8,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//8*3,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//8*5,self.player_y+5))
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,SCREEN_WIDTH//8*7,self.player_y+5))
                    pyxel.playm(6,loop=False)
            if self.BOSS.phase3:
                if 100<=self.BOSS.NowTime%240<=120:
                    if self.BOSS.NowTime%4==0:
                        self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,pyxel.rndi(5,100),self.player_y+5))
                        pyxel.playm(6,loop=False)
                elif 220<=self.BOSS.NowTime%240<=239:
                    self.Boss_fire.append(BOSS_fire(self.BOSS.x+5,self.BOSS.y+13,self.player_x+3,self.player_y+5))
                
                if 220==self.BOSS.NowTime%240:
                    pyxel.playm(7,loop=False)

            if self.BOSS.phase_f:
                if self.BOSS.end_count==48:
                    pyxel.playm(7,loop=False)
                    if self.total_score < 100000000:
                        self.total_score += 10000
                        self.score[-5] += 1

            for boss_fire in self.Boss_fire.copy():
                boss_fire.update()
                if boss_fire.x<0 or boss_fire.x>105 or boss_fire.y>150:
                    self.Boss_fire.remove(boss_fire)

            for bullet in self.Bullets.copy():
                if bullet.type==1:
                    if self.BOSS.phase1:
                        if self.BOSS.NowTime%120<100:
                            if self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+15:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
                        else:
                            if self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+18:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
                    if self.BOSS.phase2 or self.BOSS.phase3:
                        if self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+12:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
                if bullet.type==2:
                    if self.BOSS.phase1:
                        if self.BOSS.NowTime%120<100:
                            if (self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+15 or
                                self.BOSS.x+2 <= bullet.x+6 <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+15):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
                        else:
                            if (self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+18 or
                                self.BOSS.x+2 <= bullet.x+6 <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+18):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
                    if self.BOSS.phase2 or self.BOSS.phase3:
                        if (self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+12 or
                            self.BOSS.x+2 <= bullet.x <= self.BOSS.x+10 and self.BOSS.y <= bullet.y <= self.BOSS.y+12):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                if self.BOSS.HP%10==0:
                                    self.BOSS.HP-=1
                                break
        ####################################################################################################################

        #自機・弾処理##################################################################################################################
        if Damage_switch:
            if self.player_HP%30==0:
                for boss_fire in self.Boss_fire.copy():
                    if self.player_type==1:
                        if self.player_x+1 <= boss_fire.x <= self.player_x+4 and self.player_y+1 <= boss_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
                    elif self.player_type==2:
                        if self.player_x <= boss_fire.x <= self.player_x+7 and self.player_y+2 <= boss_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
        ###############################################################################################################################

    def update_phase_enemy1(self):     #敵1関連処理#
        #敵１右 配置 → 弾発射 → 敵・弾処理#####################################################################################

        #配置
        if (pyxel.frame_count - self.start_frame)%100==0:
            if len(self.Enemy1R)==0:
                self.Enemy1R.append(Enemy1(pyxel.rndi(75,90),pyxel.rndi(10,70)))
        
        #処理
        for enemy1R in self.Enemy1R.copy():
            enemy1R.update()
            if enemy1R.HP<=0:
                self.Enemy1R.remove(enemy1R)
                if self.total_score < 100000000:
                    self.total_score += 1000
                    self.score[-4] += 1
            #弾用意
            if enemy1R.start_switch:
                if (pyxel.frame_count-enemy1R.start_time)%120==105:
                    self.Enemy1R_fire.append(Enemy1_Fire(enemy1R.x+4,enemy1R.y+4,self.player_x+3,self.player_y+5))
                    pyxel.playm(6,loop=False)
        
        #弾発射
        for enemy1R_fire in self.Enemy1R_fire.copy():
            enemy1R_fire.update()
            if enemy1R_fire.x<0 or enemy1R_fire.x>105 or enemy1R_fire.y>150:
                self.Enemy1R_fire.remove(enemy1R_fire)

        #敵と弾の接触処理
        for enemy1R in self.Enemy1R.copy():
            for bullet in self.Bullets.copy():
                if enemy1R.HP%10==0:
                    if bullet.type==1:
                        if (pyxel.frame_count-enemy1R.start_time)%120>=100:
                            if enemy1R.start_switch:
                                if enemy1R.x+1 <= bullet.x <= enemy1R.x+7 and enemy1R.y+1 <= bullet.y <= enemy1R.y+7:
                                    pyxel.playm(2,loop=False)
                                    self.Bullets.remove(bullet)
                                    enemy1R.HP-=1
                                    break
                            else:
                                if enemy1R.x <= bullet.x <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5:
                                    self.Bullets.remove(bullet)
                                    break
                        else:
                            if enemy1R.x <= bullet.x <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5:
                                self.Bullets.remove(bullet)
                                break
                    elif bullet.type==2:
                        if (pyxel.frame_count-enemy1R.start_time)%120>=100:
                            if enemy1R.start_switch:
                                if (enemy1R.x+1 <= bullet.x <= enemy1R.x+7 and enemy1R.y+1 <= bullet.y <= enemy1R.y+7 or
                                    enemy1R.x+1 <= bullet.x+6 <= enemy1R.x+7 and enemy1R.y+1 <= bullet.y <= enemy1R.y+7):
                                    pyxel.playm(2,loop=False)
                                    self.Bullets.remove(bullet)
                                    enemy1R.HP-=5
                                    break
                            else:
                                if (enemy1R.x <= bullet.x <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5 or
                                    enemy1R.x <= bullet.x+6 <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5):
                                    self.Bullets.remove(bullet)
                                    break
                        else:
                            if (enemy1R.x <= bullet.x <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5 or
                                enemy1R.x <= bullet.x+6 <= enemy1R.x+7 and enemy1R.y <= bullet.y <= enemy1R.y+5):
                                self.Bullets.remove(bullet)
                                break
        ##################################################################################################################
            
        #敵１左 配置 → 弾発射 → 敵・弾処理##################################################################################

        #配置
        if (pyxel.frame_count - self.start_frame)%100==50:
            if len(self.Enemy1L)==0:
                self.Enemy1L.append(Enemy1(pyxel.rndi(5,20),pyxel.rndi(5,65)))
        
        #処理
        for enemy1L in self.Enemy1L.copy():
            enemy1L.update()
            if enemy1L.HP<=0:
                self.Enemy1L.remove(enemy1L)
                if self.total_score < 100000000:
                    self.total_score += 1000
                    self.score[-4] += 1
            #弾用意
            if enemy1L.start_switch:
                if (pyxel.frame_count-enemy1L.start_time)%120==105:
                    self.Enemy1L_fire.append(Enemy1_Fire(enemy1L.x+4,enemy1L.y+4,self.player_x+3,self.player_y+5))
                    pyxel.playm(6,loop=False)
        
        #弾発射
        for enemy1L_fire in self.Enemy1L_fire.copy():
            enemy1L_fire.update()
            if enemy1L_fire.x<0 or enemy1L_fire.x>105 or enemy1L_fire.y>150:
                self.Enemy1L_fire.remove(enemy1L_fire)

        #敵と弾の接触処理
        for enemy1L in self.Enemy1L.copy():
            for bullet in self.Bullets.copy():
                if enemy1L.HP%10==0:
                    if bullet.type==1:
                        if (pyxel.frame_count-enemy1L.start_time)%120>=100:
                            if enemy1L.start_switch:
                                if enemy1L.x+1 <= bullet.x <= enemy1L.x+7 and enemy1L.y+1 <= bullet.y <= enemy1L.y+7:
                                    pyxel.playm(2,loop=False)
                                    self.Bullets.remove(bullet)
                                    enemy1L.HP-=1
                                    break
                            else:
                                if enemy1L.x <= bullet.x <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5:
                                    self.Bullets.remove(bullet)
                                    break
                        else:
                            if enemy1L.x <= bullet.x <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5:
                                self.Bullets.remove(bullet)
                                break
                    elif bullet.type==2:
                        if (pyxel.frame_count-enemy1L.start_time)%120>=100:
                            if enemy1L.start_switch:
                                if (enemy1L.x+1 <= bullet.x <= enemy1L.x+7 and enemy1L.y+1 <= bullet.y <= enemy1L.y+7 or
                                    enemy1L.x+1 <= bullet.x+6 <= enemy1L.x+7 and enemy1L.y+1 <= bullet.y <= enemy1L.y+7):
                                    pyxel.playm(2,loop=False)
                                    self.Bullets.remove(bullet)
                                    enemy1L.HP-=5
                                    break
                            else:
                                if (enemy1L.x <= bullet.x <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5 or
                                    enemy1L.x <= bullet.x+6 <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5):
                                    self.Bullets.remove(bullet)
                                    break
                        else:
                            if (enemy1L.x <= bullet.x <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5 or
                                enemy1L.x <= bullet.x+6 <= enemy1L.x+7 and enemy1L.y <= bullet.y <= enemy1L.y+5):
                                self.Bullets.remove(bullet)
                                break
        ###################################################################################################################

        #自機・弾処理#######################################################################################################
        if Damage_switch:
            if self.player_HP%30==0:
                for enemy1R_fire in self.Enemy1R_fire.copy():
                    if self.player_type==1:
                        if self.player_x+1 <= enemy1R_fire.x <= self.player_x+4 and self.player_y+1 <= enemy1R_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
                    elif self.player_type==2:
                        if self.player_x <= enemy1R_fire.x <= self.player_x+7 and self.player_y+2 <= enemy1R_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
                for enemy1L_fire in self.Enemy1L_fire.copy():
                    if self.player_type==1:
                        if self.player_x+1 <= enemy1L_fire.x <= self.player_x+4 and self.player_y+1 <= enemy1L_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
                    elif self.player_type==2:
                        if self.player_x <= enemy1L_fire.x <= self.player_x+7 and self.player_y+2 <= enemy1L_fire.y <= self.player_y+6:
                            pyxel.playm(1,loop=False)
                            self.player_HP-=1
                            break
        ###################################################################################################################

    def update_phase_comet(self):     #隕石関連処理#
        #隕石の配置処理####################################################################################
        if (pyxel.frame_count - self.start_frame)%self.comet_interval==0:
            self.Comets.append(Comet(pyxel.rndi(1,SCREEN_WIDTH-16),-4,pyxel.rndi(3,5)/2,pyxel.rndi(1,3)))

        for comet in self.Comets.copy():
            comet.update()
            if comet.HP<=0:
                self.Comets.remove(comet)
                if self.total_score < 100000000:
                    self.total_score += comet.level*100
                    self.score[-3] += comet.level

            if comet.y > SCREEN_HEIGHT:
                self.Comets.remove(comet)
        ##################################################################################################

        #弾と隕石の衝突処理#################################################################################
        for comet in self.Comets.copy():
            for bullet in self.Bullets.copy():
                if comet.HP%10==0:
                    if bullet.type==1:
                        if comet.level==1:
                            if comet.x <= bullet.x <= comet.x+5 and comet.y <= bullet.y <= comet.y+9:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=1
                                break
                        elif comet.level==2:
                            if comet.x <= bullet.x <= comet.x+6 and comet.y <= bullet.y <= comet.y+12:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=1
                                break
                        elif comet.level==3:
                            if comet.x <= bullet.x <= comet.x+9 and comet.y <= bullet.y <= comet.y+14:
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=1
                                break
                    elif bullet.type==2:
                        if comet.level==1:
                            if (comet.x <= bullet.x <= comet.x+5 and comet.y <= bullet.y <= comet.y+9 or 
                                comet.x <= bullet.x+6 <= comet.x+5 and comet.y <= bullet.y <= comet.y+9):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=7
                                break
                        elif comet.level==2:
                            if (comet.x <= bullet.x <= comet.x+6 and comet.y <= bullet.y <= comet.y+12 or
                                comet.x <= bullet.x+6 <= comet.x+6 and comet.y <= bullet.y <= comet.y+12):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=7
                                break
                        elif comet.level==3:
                            if (comet.x <= bullet.x <= comet.x+9 and comet.y <= bullet.y <= comet.y+14 or
                                comet.x <= bullet.x+6 <= comet.x+9 and comet.y <= bullet.y <= comet.y+14):
                                pyxel.playm(2,loop=False)
                                self.Bullets.remove(bullet)
                                comet.HP-=7
                                break
        ###################################################################################################

        #ダメージ処理##################################################################################################
        if Damage_switch:
            if self.player_HP%30==0:
                for comet in self.Comets.copy():
                    #if self.player_HP%30==0:
                        if self.player_type==1:
                            if comet.level==1:
                                if comet.x-4 <= self.player_x+1 <= comet.x+5 and comet.y+0 <= self.player_y+1 <= comet.y+8:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
                            elif comet.level==2:
                                if comet.x-4 <= self.player_x+1 <= comet.x+6 and comet.y+3 <= self.player_y+1 <= comet.y+11:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
                            elif comet.level==3:
                                if comet.x-4 <= self.player_x+1 <= comet.x+9 and comet.y+3 <= self.player_y+1 <= comet.y+13:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
                        elif self.player_type==2:
                            if comet.level==1:
                                if comet.x-6 <= self.player_x+1 <= comet.x+5 and comet.y+0 <= self.player_y+3 <= comet.y+8:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
                            elif comet.level==2:
                                if comet.x-6 <= self.player_x+1 <= comet.x+6 and comet.y+3 <= self.player_y+3 <= comet.y+11:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
                            elif comet.level==3:
                                if comet.x-6 <= self.player_x+1 <= comet.x+9 and comet.y+3 <= self.player_y+3 <= comet.y+13:
                                    pyxel.playm(1,loop=False)
                                    self.player_HP -= 1
                                    break
            else:
                self.player_HP-=1
        ###############################################################################################################

    def update_play_scene(self):
        pyxel.mouse(False)
        if self.play_interval==0:

            ############ー開始フレーム取得ー##############
            if self.start_switch == "off":
                if (pyxel.btnp(pyxel.KEY_F) or 
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)):
                    self.start_frame = pyxel.frame_count
                    self.start_switch = "on"
                    self.Game_start = True
                    self.phase_one = True
                    pyxel.playm(4,loop=True)
            ############################################

        #弾の発射処理#####################################################
            if (pyxel.btnp(pyxel.KEY_F) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)):
                pyxel.playm(0,loop=False)
                if self.player_type==1:
                    self.Bullets.append(Bullet(self.player_x + 3,127,self.player_type))
                elif self.player_type==2:
                    self.Bullets.append(Bullet(self.player_x + 1,132,self.player_type))

        for bullet in self.Bullets.copy():
            bullet.update()

            if bullet.y <= -3:
                self.Bullets.remove(bullet)
        #################################################################

        #自機の移動処理###########################################################
        if self.player_type==1:
            if self.Game_start:
                if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.player_x > 1:
                    self.player_x-=1.5
                if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.player_x < SCREEN_WIDTH - 8:
                    self.player_x+=1.5
        elif self.player_type==2:
            if self.Game_start:
                if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.player_x > 1:
                    self.player_x-=2
                if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.player_x < SCREEN_WIDTH - 10:
                    self.player_x+=2
        #########################################################################

        if self.phase_one:
            self.update_phase_comet()
        if self.phase_two:
            self.update_phase_enemy1()
        if self.phase_three:
            self.update_boss()

        #スコア処理###################################
        if self.total_score < 100000000:
            for i in range(len(self.score)-3,0,-1):
                x,y = divmod(self.score[i],10)
                self.score[i] = y
                self.score[i-1] += x
            if self.score[0] >= 10:
                self.score = [9,9,9,9,9,9,9,9]

        if PHASE3_SCORE > self.total_score >= PHASE2_SCORE:
            self.comet_interval = 30
            self.phase_two = True
        elif self.total_score >= PHASE3_SCORE:
            self.comet_interval = 50
            if self.BOSS==0:
                self.phase_three = True
        #############################################

    #スタート画面########################################################################
    def update_start_scene(self):
        pyxel.mouse(True)
        if self.ranking_switch=="off":
            if self.change_scene==30 or self.change_scene==0:
                if (pyxel.btnp(pyxel.KEY_SPACE) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)):
                    pyxel.playm(5,loop=False)
                    self.current_scene = PLAY_SCENE
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    if 2 <= pyxel.mouse_x <= 13 and 2 <= pyxel.mouse_y <= 13:
                        self.ranking_switch = "on"

            #キャラクターチェンジ処理#########################################################
            if self.player_unlock1:
                if self.Player_Change==False:
                    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                        self.Player_Change = True
                        self.change_scene -= 1
                        self.player_type = 2
                        self.player_x -= 1
                        self.type_number = 1
                        self.type_list.append(2)
                        
                        with open(self.kinds_path,"w") as x:
                            x.write(" ".join(map(str,self.type_list)))

                if 1 <= self.change_scene <= 29:
                    self.change_scene -= 1
            
            if len(self.type_list)>=2:            
                if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                    if self.type_number==len(self.type_list)-1:
                        self.type_number=0
                        self.player_type=self.type_list[self.type_number]
                    else:
                        self.type_number+=1
                        self.player_type=self.type_list[self.type_number]
                elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                    if self.type_number==0:
                        self.type_number=len(self.type_list)-1
                        self.player_type=self.type_list[self.type_number]
                    else:
                        self.type_number-=1
                        self.player_type=self.type_list[self.type_number]
            ###############################################################################

            
        
        else:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if 2 <= pyxel.mouse_x <= 13 and 2 <= pyxel.mouse_y <= 13:
                    self.ranking_switch = "off"
                    
        if self.player_type==1:
            self.player_x=SCREEN_WIDTH//2-3
        elif self.player_type==2:
            self.player_x=SCREEN_WIDTH//2-4

    ###################################################################################


    def update(self):
        #ゲーム終了処理
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            pyxel.quit()

        #ゲームオーバー＆リセット処理##################
        if self.GAME_OVER:
            if self.gameover_time<=158:
                self.gameover_time+=1
            else:
                self.current_scene = START_SCENE
                self.current_phase = ""
                self.phase_one = False
                self.phase_two = False
                self.phase_three = False
                self.BOSS = 0

                self.player_x = SCREEN_WIDTH//2-3
                self.player_y = 130
                self.player_HP = P_HP
                self.player_type = 1
                self.type_number = 0
                self.change_scene = 30

                self.play_interval = 40
                self.start_frame = 0
                self.score = SCORE.copy()
                self.total_score = T_SCORE

                self.Bullets = []
                self.Comets = []
                self.Enemy1R = []
                self.Enemy1R_fire = []
                self.Enemy1L = []
                self.Enemy1L_fire = []
                self.Boss_fire = []
                
                self.comet_interval = 20

                self.start_switch = "off"

                self.Game_start = False
                self.GAME_OVER = False
                self.gameover_time = -1
        ##############################################


        if self.player_HP>=0:
            #背景配置処理###############################################
            self.backgroundA1_y = pyxel.frame_count % 150
            self.backgroundA2_y = pyxel.frame_count % 150 - 150
            self.backgroundB1_y = pyxel.frame_count % 150 * 1.5
            self.backgroundB2_y = pyxel.frame_count % 150 * 1.5 - 225
            self.backgroundC1_y = pyxel.frame_count % 150 * 2
            self.backgroundC2_y = pyxel.frame_count % 150 * 2 - 150
            self.backgroundC3_y = pyxel.frame_count % 150 * 2 - 300
            self.backgroundC4_y = pyxel.frame_count % 150 * 2 - 450
            ###########################################################

        #シーン切り替え#######################
        if self.current_scene==START_SCENE:
            self.update_start_scene()

        elif self.current_scene==PLAY_SCENE:
            if self.player_HP>=0:
                self.update_play_scene()
        #####################################

        #ゲームオーバー進行処理###########################
        if self.player_HP<0:
            self.GAME_OVER = True
            if self.gameover_time==-1:
                self.gameover_frame = pyxel.frame_count
                self.gameover_time+=1
                pyxel.stop()
                pyxel.playm(3,loop=False)
                
                if self.total_score>=5000:
                    self.player_unlock1 = True

                self.score_ranking.append(self.score)
                self.score_ranking = sorted(self.score_ranking,reverse=True)
                if len(self.score_ranking)>=6:self.score_ranking.pop()
                self.first = self.score_ranking[0]
                if len(self.score_ranking)>=2:self.second = self.score_ranking[1]
                if len(self.score_ranking)>=3:self.third = self.score_ranking[2]
                if len(self.score_ranking)>=4:self.fourth = self.score_ranking[3]
                if len(self.score_ranking)>=5:self.fifth = self.score_ranking[4]
                
                #データの上書き#########################################################
                with open(self.score_path,"w") as x:
                    for i in range(len(self.score_ranking)):
                            x.write(" ".join(map(str,self.score_ranking[i])) + "\n")
                #######################################################################
                                
        ################################################

#描画
    def draw_BOSS(self):
        if not self.BOSS==0:
            self.BOSS.draw()
        for boss_fire in self.Boss_fire:
            boss_fire.draw()

    def draw_phase_enemy1(self):
            ###################################################################################
            for enemy1R in self.Enemy1R:
                if not self.GAME_OVER:
                    enemy1R.draw()
                else:
                    if enemy1R.HP%2==0:
                        if enemy1R.y < enemy1R.end_y:
                            if self.gameover_frame%20<10:
                                pyxel.blt(enemy1R.x,enemy1R.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                            else:
                                pyxel.blt(enemy1R.x,enemy1R.y,0,122,16,8,8,pyxel.COLOR_BLACK)
                        else:
                            if (self.gameover_frame-enemy1R.start_time)%120>=100:
                                if self.gameover_frame%20<10:
                                    pyxel.blt(enemy1R.x,enemy1R.y,0,24,0,9,9,pyxel.COLOR_BLACK)
                                else:
                                    pyxel.blt(enemy1R.x,enemy1R.y,0,112,16,9,9,pyxel.COLOR_BLACK)
                            else:
                                if self.gameover_frame%20<10:
                                    pyxel.blt(enemy1R.x,enemy1R.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                                else:
                                    pyxel.blt(enemy1R.x,enemy1R.y,0,122,16,8,8,pyxel.COLOR_BLACK)
            for enemy1L in self.Enemy1L:
                if not self.GAME_OVER:
                    enemy1L.draw()
                else:
                    if enemy1L.HP%2==0:
                        if enemy1L.y < enemy1L.end_y:
                            if self.gameover_frame%20<10:
                                pyxel.blt(enemy1L.x,enemy1L.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                            else:
                                pyxel.blt(enemy1L.x,enemy1L.y,0,122,16,8,8,pyxel.COLOR_BLACK)
                        else:
                            if (self.gameover_frame-enemy1L.start_time)%120>=100:
                                if self.gameover_frame%20<10:
                                    pyxel.blt(enemy1L.x,enemy1L.y,0,24,0,9,9,pyxel.COLOR_BLACK)
                                else:
                                    pyxel.blt(enemy1L.x,enemy1L.y,0,112,16,9,9,pyxel.COLOR_BLACK)
                            else:
                                if self.gameover_frame%20<10:
                                    pyxel.blt(enemy1L.x,enemy1L.y,0,34,0,8,8,pyxel.COLOR_BLACK)
                                else:
                                    pyxel.blt(enemy1L.x,enemy1L.y,0,122,16,8,8,pyxel.COLOR_BLACK)
            for enemy1R_fire in self.Enemy1R_fire:
                if not self.GAME_OVER:
                    enemy1R_fire.draw()
                else:
                    if self.gameover_frame%4<=1:
                        pyxel.blt(enemy1R_fire.x,enemy1R_fire.y,0,28,11,2,2)
                    else:
                        pyxel.blt(enemy1R_fire.x,enemy1R_fire.y,0,31,11,2,2)
            for enemy1L_fire in self.Enemy1L_fire:
                if not self.GAME_OVER:
                    enemy1L_fire.draw()
                else:
                    if self.gameover_frame%4<=1:
                        pyxel.blt(enemy1L_fire.x,enemy1L_fire.y,0,28,11,2,2)
                    else:
                        pyxel.blt(enemy1L_fire.x,enemy1L_fire.y,0,31,11,2,2)
            ####################################################################################
 
    def draw_phase_comet(self):

        #隕石の描画処理############
        for comet in self.Comets:
            comet.draw()
        ##########################

    def draw_play_scene(self):
        #開始時処理########################################################################################
        if self.play_interval>0:
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-10,"Shooting Game",pyxel.COLOR_WHITE)
            if self.play_interval>10:
                if self.play_interval%10<5:
                    pyxel.text(SCREEN_WIDTH//2-20,SCREEN_HEIGHT//2+5,"Press Space",pyxel.COLOR_WHITE)
                self.play_interval-=1
            else:
                self.play_interval-=1
            return

        if self.Game_start==False:
            pyxel.text(SCREEN_WIDTH//2-27,SCREEN_HEIGHT//2-10,"Press 'F'ire!!",pyxel.COLOR_WHITE)
        ##################################################################################################

        #弾の描画処理##############
        for bullet in self.Bullets:
            bullet.draw()
        ##########################

    def draw_start_scene(self):
        #スタート画面描画######################################################################
        pyxel.blt(2,2,0,121,0,12,12,pyxel.COLOR_BLACK)
        if self.ranking_switch=="off":
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-10,"Shooting Game",pyxel.COLOR_WHITE)
            if pyxel.frame_count % 30 < 15:
                pyxel.text(SCREEN_WIDTH//2-20,SCREEN_HEIGHT//2+5,"Press Space",pyxel.COLOR_WHITE)
            if len(self.type_list)>=2:
                pyxel.blt(35,132,0,146,1,3,5,pyxel.COLOR_BLACK)
                pyxel.blt(67,132,0,146,9,3,5,pyxel.COLOR_BLACK)
        if self.ranking_switch=="on":
            pyxel.blt(SCREEN_WIDTH//2-32,SCREEN_HEIGHT//2-42,0,114,2,6,5,pyxel.COLOR_BLACK)
            pyxel.blt(SCREEN_WIDTH//2+28,SCREEN_HEIGHT//2-42,0,114,2,6,5,pyxel.COLOR_BLACK)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-42,"SCORE RANKING",pyxel.COLOR_WHITE)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-30,f"1st  {"".join(map(str,self.first))}",pyxel.COLOR_ORANGE)
            pyxel.blt(SCREEN_WIDTH//2-32,SCREEN_HEIGHT//2-29.5,0,138,2,5,4,pyxel.COLOR_BLACK)
            if pyxel.frame_count%10<5:
                pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-30,f"1st  {"".join(map(str,self.first))}",pyxel.COLOR_YELLOW)
                pyxel.blt(SCREEN_WIDTH//2-32,SCREEN_HEIGHT//2-29.5,0,138,6,5,4,pyxel.COLOR_BLACK)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-20,f"2nd  {"".join(map(str,self.second))}",pyxel.COLOR_GRAY)
            if pyxel.frame_count%10<5:
                pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-20,f"2nd  {"".join(map(str,self.second))}",pyxel.COLOR_WHITE)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-10,f"3rd  {"".join(map(str,self.third))}",pyxel.COLOR_BROWN)
            if pyxel.frame_count%10<5:
                pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2-10,f"3rd  {"".join(map(str,self.third))}",pyxel.COLOR_ORANGE)
            pyxel.text(SCREEN_WIDTH//2-29,SCREEN_HEIGHT//2,"---------------",pyxel.COLOR_WHITE)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2+10,f"4th  {"".join(map(str,self.fourth))}",pyxel.COLOR_WHITE)
            pyxel.text(SCREEN_WIDTH//2-25,SCREEN_HEIGHT//2+20,f"5th  {"".join(map(str,self.fifth))}",pyxel.COLOR_WHITE)
        ######################################################################################      

    def draw(self):
        #背景描画処理######################################################
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundA1_y,0,1,17,105,150,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundA2_y,0,1,17,105,150,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundB1_y,1,1,17,105,225,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundB2_y,1,1,17,105,225,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundC1_y,2,1,17,105,150,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundC2_y,2,1,17,105,150,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundC3_y,2,1,17,105,150,pyxel.COLOR_BLACK)
        pyxel.blt(0,self.backgroundC4_y,2,1,17,105,150,pyxel.COLOR_BLACK)
        ##################################################################

        #自機描画処理###############################################################
        if self.player_type==1:
            if self.player_HP%2==0:
                if pyxel.frame_count % 10 < 5:
                    pyxel.blt(self.player_x,self.player_y,0,8,0,7,9,pyxel.COLOR_BLACK)
                else:
                    pyxel.blt(self.player_x,self.player_y,0,16,0,7,10,pyxel.COLOR_BLACK)
            elif self.player_HP==-1:
                if self.gameover_frame % 10 < 5:
                    pyxel.blt(self.player_x,self.player_y,0,8,0,7,9,pyxel.COLOR_BLACK)
                else:
                    pyxel.blt(self.player_x,self.player_y,0,16,0,7,10,pyxel.COLOR_BLACK)
        elif self.player_type==2:
            if self.player_HP%2==0:
                if pyxel.frame_count % 10 < 5:
                    pyxel.blt(self.player_x,self.player_y,0,88,0,9,9,pyxel.COLOR_BLACK)
                else:
                    pyxel.blt(self.player_x,self.player_y,0,104,0,9,10,pyxel.COLOR_BLACK)
            elif self.player_HP==-1:
                if self.gameover_frame % 10 < 5:
                    pyxel.blt(self.player_x,self.player_y,0,88,0,9,9,pyxel.COLOR_BLACK)
                else:
                    pyxel.blt(self.player_x,self.player_y,0,104,0,9,10,pyxel.COLOR_BLACK)
        ###########################################################################

        #シーン切り替え########################
        if self.current_scene==START_SCENE:
            self.draw_start_scene()

        elif self.current_scene==PLAY_SCENE:
            self.draw_play_scene()
        ######################################

        #フェーズ切り替え###################
        if self.phase_two:
            self.draw_phase_enemy1()
        if self.phase_one:
            self.draw_phase_comet()
        if self.phase_three:
            self.draw_BOSS()
        ###################################

        #UI表示
        if self.Game_start:
            #スコア表示################################################################
            pyxel.text(50,1,f"SCORE:{"".join(map(str,self.score))}",pyxel.COLOR_WHITE)
            ##########################################################################

            #残機表示######################################################
            if self.player_type==1:
                if self.player_HP>=0:
                    pyxel.blt(1,SCREEN_HEIGHT-7,0,2,10,5,6,pyxel.COLOR_BLACK)
                if self.player_HP>=30:
                    pyxel.blt(7,SCREEN_HEIGHT-7,0,2,10,5,6,pyxel.COLOR_BLACK)
                if self.player_HP>=60:
                    pyxel.blt(13,SCREEN_HEIGHT-7,0,2,10,5,6,pyxel.COLOR_BLACK)
            elif self.player_type==2:
                if self.player_HP>=0:
                    pyxel.blt(1,SCREEN_HEIGHT-7,0,89,10,7,6,pyxel.COLOR_BLACK)
                if self.player_HP>=30:
                    pyxel.blt(9,SCREEN_HEIGHT-7,0,89,10,7,6,pyxel.COLOR_BLACK)
                if self.player_HP>=60:
                    pyxel.blt(17,SCREEN_HEIGHT-7,0,89,10,7,6,pyxel.COLOR_BLACK)
            ###############################################################
            

        #ゲームオーバー描画#######################################################################
        if self.GAME_OVER:
            if self.gameover_time%40<20:
                pyxel.text(SCREEN_WIDTH//2-18,SCREEN_HEIGHT//2-7,"GAME OVER",pyxel.COLOR_WHITE)
            if self.total_score >= 5000:
                if self.gameover_time%40<20 and self.gameover_time%4<2:
                    pyxel.text(SCREEN_WIDTH//2+2,SCREEN_HEIGHT//2-7,"OVER",pyxel.COLOR_YELLOW)
        #########################################################################################
        
        if 1 <= self.change_scene <= 29:
            pyxel.cls(pyxel.COLOR_BLACK)



App()