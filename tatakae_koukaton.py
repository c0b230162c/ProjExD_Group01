import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
bg_img = pg.image.load(f"fig/pg_bg.jpg")  #初期背景


class GameOver:
    def __init__(self):  #初期設定
        self.background = pg.Surface((WIDTH,HEIGHT))
        self.shikaku = pg.Surface((WIDTH,HEIGHT))
        self.shikaku.set_alpha(200)
        self.bird =  pg.image.load(f"fig/yorokobi.png")
        self.fonto1 = pg.font.SysFont("hgp明朝b",250)
        self.fonto2 = pg.font.SysFont("hgp明朝b", 30)
        self.txt1 = self.fonto1.render("GAME OVER",True,(255,255,255))
        self.txt2 = self.fonto2.render("Enterでtitleに戻る", True, (255, 255, 255))
    def all_blit(self):  #貼り付け系
        pg.draw.rect(self.background,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
        pg.draw.rect(self.shikaku,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
        screen.blit(self.background,(0,0))
        screen.blit(self.bird,(WIDTH/2,HEIGHT/20))
        screen.blit(self.shikaku,(0,0))
        screen.blit(self.txt1,[WIDTH/18,HEIGHT/3])
        screen.blit(self.txt2,[500,HEIGHT-HEIGHT/5])
        pg.display.update()

class Ending:
    def __init__(self, img):  #初期設定
        self.shikaku = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(self.shikaku,(255,255,255),pg.Rect(0,0,WIDTH,HEIGHT))
        self.shikaku.set_alpha(128)
        self.image3 = pg.Surface((WIDTH-200, HEIGHT-500))#メッセージボックス
        pg.draw.rect(self.image3,(0,0,0),(0,0,WIDTH,HEIGHT))
        self.rect3 = self.image3.get_rect()
        self.rect3.center = WIDTH/2,HEIGHT-(HEIGHT/4)
        self.fonto1 = pg.font.SysFont("hgp明朝b",200)
        self.fonto2 = pg.font.SysFont("hg正楷書体pro", 40)
        self.txt1 = self.fonto1.render("The End",True,(0,0,0))
        self.txt2 = self.fonto2.render("こうかとんは正気を取り戻し、手下たちは我に返った。",True,(255,255,255))
        self.txt3 = self.fonto2.render("奪われていた単位と学部長賞は学生のもとに返された。",True,(255,255,255))
        self.txt4 = self.fonto2.render("こうして東京工科大学に再び平穏が訪れたのであった。",True,(255,255,255))
        self.ed_img = img
    def blit_1(self):  #あとがき表示
        screen.blit(self.ed_img, [0, 0])
        screen.blit(self.shikaku,(0,0))
        screen.blit(self.image3,self.rect3)
        screen.blit(self.txt2,[WIDTH/10,470])
        screen.blit(self.txt3,[WIDTH/10,550])
        screen.blit(self.txt4,[WIDTH/10,630])
        pg.display.update()
    def blit_2(self):  #「The　End」表示
        screen.blit(self.ed_img, [0, 0])
        screen.blit(self.shikaku,(0,0))
        screen.blit(self.txt1,[WIDTH/5,HEIGHT/3])
        pg.display.update()
    
def Opening(): #Opening画面（仮置き）
    print("opening")

def main():
    mode = "Ending"
    ed_img = pg.image.load(f"fig/ending.png") #Ending用背景
    go = GameOver()
    ed = Ending(ed_img)
    while True:
        screen.blit(bg_img, [0, 0]) #初期背景貼り付け
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if mode == "GameOver":  #modeがGameOverの時
            go.all_blit()       #GameOverクラスのall_blitを呼び出す
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:  #キーが押されているとき
                        if event.key == pg.K_RETURN: #enterキーが押されたとき
                            mode = "title"  #modeをtitleにする
                            waiting = False
                            break
                    elif event.type == pg.QUIT:
                        pg.quit()
                        sys.exit(0) 

        if mode == "Ending":  #modeがEnding1の時
            ed.blit_1()     #Endingクラスのblit_1を呼び出す
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:  #キーが押されているとき
                        if event.key == pg.K_RETURN: #enterキーが押されたとき
                            mode = "Ending2"   #modeをEndingにする
                            waiting = False
                            break
                    elif event.type == pg.QUIT:
                        pg.quit()
                        sys.exit(0) 
        if mode == "Ending2":  #modeがEnding2の時
            ed.blit_2()  #Endingクラスのblit_2を呼び出す
        if mode == "title": 
            Opening()
        pg.display.update()
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()