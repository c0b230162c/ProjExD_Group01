import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800
mode = "マップ" #modeで画面切り替え
battle = 1 #バトルモードの時、攻撃があった場合

def load_sound(file):
    """
    音源を読み込む関数
    引数1 file：音源ファイル
    """
    if not pg.mixer:
        return None
    
    try:
        sound = pg.mixer.Sound(file) #Soundオブジェクト作成
        return sound
    except pg.error:
        print(f"Warning, unable to load,{file}")
    
    return None


class Synopsis:
    """
    あらすじ画面に関するクラス
    """

    #あらすじリスト
    syp_lst = [
        "20××年、東京工科大学のマスコットキャラの,こうかとんが何らかの力によって邪悪な存在へと,変貌してしまった。", 
        "邪悪な存在となったこうかとんは学生の単位と学部長賞を奪っていった。", 
        "そこで立ち上がったのは、プロジェクト演習Dチーム3であった。", 
        "こうかとんの手下とこうかとんを倒すため、いざ出陣！"
    ]

    def __init__(self):
        """
        あらすじに必要な、背景写真・メッセージボックス・あらすじ文を生成する
        """
        self.image = pg.image.load("fig/kouka.jpg")  #タイトルと同じ画像
        self.rect = self.image.get_rect()

        self.image2 = pg.Surface((WIDTH, HEIGHT)) #透明な四角
        pg.draw.rect(self.image2, (0,0,0), (0,0,WIDTH, HEIGHT))
        self.rect2 = self.image2.get_rect()
        self.image2.set_alpha(128)

        self.image3 = pg.Surface((WIDTH-200, HEIGHT-600)) #メッセージボックス
        pg.draw.rect(self.image3, (0,0,0), (0,0,WIDTH, HEIGHT))
        self.rect3 = self.image3.get_rect()
        self.rect3.center = WIDTH/2, HEIGHT-(HEIGHT/6)

        self.font = pg.font.SysFont("hg正楷書体pro",40)
        self.index = 0  #表示文字のインデックス
        # self.num = 1  #フェードアウト確認用

    
    def key_event(self, event):
        """
        エンターキーが押されたかを判定
        モードの切り替え
        """
        global mode
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.index += 1
            self.image3.fill((0,0,0)) #リセット
            if self.index >= len(__class__.syp_lst):
                self.index = 0
                self.num = 0
                mode = "バトル"   #変更
                print("次のモード")
        return True
    

    def update(self, screen:pg.Surface):
        """
        あらすじ文字の表示
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.image2, self.rect2)
        screen.blit(self.image3, self.rect3)

        y_off = 10
        high = 40

        if self.index < len(__class__.syp_lst):
            text = __class__.syp_lst[self.index]
            for i in range(0, len(text), 25):
                line = text[i:i+25]
                self.txt = self.font.render(line, True, (255,255,255,))
                self.image3.blit(self.txt, [10, y_off])
                y_off += high


def main():
    global mode
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    synopsis = None #初期値
    
    #mode切り替え
    if mode == "オープニング":
        op_bgm = load_sound("sound/op_bgm.mp3")
        op_bgm.play()
    elif mode == "あらすじ":
        synopsis = Synopsis()
        syp_bgm = load_sound("sound/syp_bgm.mp3")
        syp_bgm.play()
        # if synopsis.num == 0:
            # syp_bgm.fadeout(10)  #フェードアウト
    elif mode == "マップ":
        map_bgm = load_sound("sound/map_bgm.mp3")
        map_bgm.play()
    elif mode == "バトル":
        battle_bgm = load_sound("sound/battle_bgm.mp3")
        battle_bgm.play()
        if battle == 1: #攻撃が行われたとき
            panch = load_sound("sound/panch.mp3") #ループなし
            panch.play()
    elif mode == "エンディング":
        ed_bgm = load_sound("sound/ed_bgm.mp3")
        ed_bgm.play()
    elif mode == "ゲームオーバー":
        gameover = load_sound("sound/gameover.mp3") #ループなし
        gameover.play()


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

            if mode == "あらすじ" and synopsis:
                if not synopsis.key_event(event):
                    pg.quit()
                    sys.exit()
            # 他のモードの場合のイベント処理をここに追加


        if mode == "あらすじ" and synopsis:
            synopsis.update(screen)


        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()