import os
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800


def main():
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg = pg.image.load(f"fig/kena-xga.jpg").convert_alpha()
    bg = pg.transform.scale(bg, (WIDTH,HEIGHT)) 
    shikaku = pg.Surface((WIDTH,HEIGHT))
    shikaku_rect = pg.draw.rect(shikaku,(255,255,255),pg.Rect(0,0,WIDTH,HEIGHT))
    shikaku.set_alpha(128)
    #opning = pg.sprite.Group()
    gamemode = "0" #ゲームモードを０に設定する
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return 
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN: #もしエンターキーが押されたら
                gamemode = "1" #ゲームモードを1にする
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE: #もしエンターキーが押されたら
                gamemode = "2"

                
        if gamemode == "0": #もしゲームモードが0ならば
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            img1 = fonto1.render("倒せこうかとん", 0, (0, 0, 0)) #タイトル
            screen.blit(bg,[0,0]) #背景画像
            screen.blit(shikaku, shikaku_rect)
            screen.blit(img1, [400, 150])
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
            img2 = fonto2.render("Press enter to Start", 0, (0, 255, 255))
            screen.blit(img2, [450, 400])
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (400, 400)) 
            screen.blit(cha1,[-50,400]) #キャラクター1
            cha2 = pg.image.load(f"fig/PL6.png").convert_alpha()
            cha2 = pg.transform.scale(cha2, (400, 400)) 
            screen.blit(cha2,[190,400]) #キャラクター2
            cha3 = pg.image.load(f"fig/pl5.png").convert_alpha()
            cha3 = pg.transform.scale(cha3, (400, 400)) 
            screen.blit(cha3,[430,400]) #キャラクター3
            cha4 = pg.image.load(f"fig/chibi_20240527_185904.png").convert_alpha()
            cha4 = pg.transform.scale(cha4, (400, 400)) 
            screen.blit(cha4,[670,400]) #キャラクター4
            cha5 = pg.image.load(f"fig/chibi_20240527_181131.png").convert_alpha()
            cha5 = pg.transform.scale(cha5, (400, 400)) 
            screen.blit(cha5,[910,400]) #キャラクター5
            fonto3 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
            img3 = fonto3.render("キャラクタープロフィール:shift", 0, (255, 0, 255))
            screen.blit(img3, [350, 700])
            pg.display.update()

        elif gamemode == "1": #もしゲームモードが1ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            img = fonto.render("あらすじ", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(img, [400, 250]) #あらすじ表示
            pg.display.update()
        
        elif gamemode == "2": #もしゲームモードが2ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara1name = fonto.render("さゆか", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara1name, [400, 250]) #chara1name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara1pro = fonto1.render("しっかり者のお姉さん系、ベーシスト。", 0, (0, 0, 0))
            screen.blit(chara1pro, [400, 400]) #chara1pro表示
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (500, 500))
            screen.blit(cha1,[0,200]) #キャラクター1 
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return 
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "3"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "6"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "3": #もしゲームモードが3ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara2name = fonto.render("せいな", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara2name, [400, 250]) #chara2name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara2pro = fonto1.render("冷静そうで熱い何かを持っている。", 0, (0, 0, 0))
            screen.blit(chara2pro, [400, 400]) #chara2pro表示
            chara2pro = fonto1.render("チームのまとめ役。", 0, (0, 0, 0))
            screen.blit(chara2pro, [400, 470]) #chara2pro表示
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return 
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "4"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "2"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "4": #もしゲームモードが4ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara3name = fonto.render("こうた", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara3name, [400, 250]) #chara3name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara3pro = fonto1.render("頭がおかしい。ギャグを言う。", 0, (0, 0, 0))
            screen.blit(chara3pro, [0, 250]) #chara3pro表示
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "5"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "3"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "5": #もしゲームモードが5ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara4name = fonto.render("ほのか", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara4name, [400, 250]) #chara4name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara4pro = fonto1.render("ずっと泣いている。心優しい女の子", 0, (0, 0, 0))
            screen.blit(chara4pro, [400, 400]) #chara4pro表示
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (000, 250)) 
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "6"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "4"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"

        elif gamemode == "6": #もしゲームモードが6ならば
            fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            chara5name = fonto.render("まの", 0, (0, 0, 0))
            screen.blit(bg,[0,0])
            screen.blit(shikaku, shikaku_rect)
            screen.blit(chara5name, [400, 250]) #chara5name表示
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
            chara5pro = fonto1.render("落ち着きない人。", 0, (0, 0, 0))
            screen.blit(chara5pro, [400, 400]) #chara5pro表示
            screen.blit(cha1,[0,250]) #キャラクター5
            cha2 = pg.image.load(f"fig/chibi_20240527_181131.png").convert_alpha()
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "2"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "5"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "0"
                    

            

        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()