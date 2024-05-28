import os
import time
import pygame as pg
import random
import sys


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800   #ディスプレイの大きさ
battle = 1 #バトルモードの時、攻撃があった場合
mode_a = ""
mode_aa = 0

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


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    Rectの画面内外判定用の関数
    引数：プレイヤーRect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:   # 横方向のはみ出し判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


def check_bound2(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    Rectの画面内外判定用の関数
    引数：プレイヤーRect
    戻り値：左方向判定結果，右方向判定結果，上方向判定結果，下方向判定結果（True：画面内／False：画面外）
    """
    ue, hidari, sita, migi = True, True, True, True
    if obj_rct.left < 0:        # 左方向のはみ出し判定
        hidari = False
    if WIDTH < obj_rct.right:   # 右方向のはみ出し判定
        migi = False
    if obj_rct.top < 0:         # 上方向のはみ出し判定
        ue = False
    if HEIGHT < obj_rct.bottom: # 下方向のはみ出し判定
        sita = False
    return ue, hidari, sita, migi


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
        global mode_a
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.index += 1
            self.image3.fill((0,0,0)) #リセット
            if self.index >= len(__class__.syp_lst):
                self.index = 0
                self.num = 0
                mode_a = "マップ"   #変更
                mode_aa = 1
                print("a")
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


class Map:
    """
    Mapの描画に関するクラス。
    """
    map_scene_xy = [(-240, -280), (-240, -200), (-240, -120), (-240, -50), (-150, -50), (-180, -20), (-40, -20), (-50, -140), (-160, -180), (-160, -250), (-320, -60), (-380, -70)]
    map_scnen_name = ["片桐研究所", "坂道", "坂の上", "研究所A&B", "講義棟A&講義実験棟", "マック", "体育館", "運動場", "FOOS FOO", "FOOS FOO 2", "講義棟C", "メディアホール"]
    img_zoom = 10.0
    def __init__(self) -> None:
        self.image = pg.image.load(f"fig/tut_map.jpg")
        self.img = pg.transform.rotozoom(self.image, 0, __class__.img_zoom)
        self.scene_num = 0
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)

    def update(self, screen, score):
        screen.blit(self.img, [__class__.map_scene_xy[self.scene_num][0]*__class__.img_zoom, 
                               __class__.map_scene_xy[self.scene_num][1]*__class__.img_zoom])
        
        # 今いる場所の表示(左上)
        self.txt = self.font.render(__class__.map_scnen_name[self.scene_num], True, (0, 0, 0))
        self.txt_rect = self.txt.get_rect()
        self.txt_rect.center = 250, 80
        screen.blit(self.txt, self.txt_rect)

        # スコアの表示(左上)
        self.txt3 = self.font.render(f"単位数：{score}", 0, (255, 0, 0))
        self.txt_rect = self.txt3.get_rect()
        self.txt_rect.center = 1100, 80
        screen.blit(self.txt3, self.txt_rect)
        

class Novel:
    """
    map下部に語り文を表示させるクラス。
    """
    nl = ["せいな：", "こうた：", "さゆか：", "まの：", "ほのか："] # プレイヤーの名前の表示
    # 表示させる語り文
    novel_lst = [[[f"{nl[0]}着いた！！片桐研究所だ！", f"{nl[4]}うえーーーーん", ""], 
                  [f"{nl[2]}今回の私達の目的は単位を拾って", "こうかとんを倒すことよ！！", ""], 
                  [f"{nl[3]}じゃあここらへんで単位をさがすか～！", "", ""]],
                 [[f"{nl[2]}ここは庭だね、、、", "", ""], 
                  [f"{nl[0]}特になにもなさそうだね、、、", "", ""], 
                  [f"{nl[1]}でも、横にはFOOS FOOがあるよ！！", "", ""]],
                 [[f"{nl[0]}坂の上は人が多いね、、、", "", ""], 
                  [f"{nl[2]}あそこみて！！！何かいるよ！！！", "いってみようよ！", ""], 
                  [f"{nl[1]}行きたくないんだけどな、、、", "", ""]],
                 [[f"{nl[2]}ここはCSで有名な研究所だね？", "ちょっとこわい、、", ""], 
                  [f"{nl[0]}なかにはいってみようか！！！", "、、、いや入り口になんかいない？？？", ""], 
                  [f"{nl[3]}多分気のせい！！！はなしかけて", "みよう！！", ""]],
                 [[f"{nl[0]}英語のにおいがするな", "", ""], 
                  [f"{nl[3]}うわ、講義室の場所に来ただけでにおう", "とか、、、英語狂人じゃん", ""], 
                  [f"{nl[0]}黙れ", "", ""], [f"{nl[2]}ところで、ここには何もなくない？？？", "", ""]],
                 [[f"{nl[3]}うわあああ不健康だぁぁぁぁぁ", "", ""], 
                  [f"{nl[4]}うええええええん", "", ""], 
                  [f"{nl[2]}そんなことより単位を探さないと！！！", "", ""]],
                 [[f"{nl[3]}健康だね！！！運動ができるよみんな", "私はしないけど、、、", ""], 
                  [f"{nl[2]}ほら、あそこに運動しがいがあるもの", "がいるよ！！", ""], 
                  [f"{nl[1]}どうせまた単位と戦わなきゃいけな", "いんでしょ", ""]],
                 [[f"{nl[2]}運動場だ！！広いね！！！", "", ""], 
                  [f"{nl[1]}ほんとに！！！！砂漠の中からアリを", "さがすくらい難しいね", ""], 
                  [f"{nl[0]}何言ってんの？", "", ""], [f"{nl[2]}喧嘩しないで", "", ""]],
                 [[f"{nl[0]}ふーず・ふーだ！！！", "", ""], 
                  ["工科大の広告をしておこう。東京工科大学で", "は校内に吉野家、\
                   マック、セブンなど沢山のご", "はん屋さんがある。大学行くなら工科大！！"], 
                  [f"{nl[1]}これで工科大の宣伝に効果大だね！！", "", ""], 
                  [f"{nl[3]}hhh", "", ""]],
                 [[f"{nl[0]}画面が少しも動いてないじゃん！！", "", ""], 
                  [f"{nl[2]}こうゆうときこそなにか大事なものが", "", ""], 
                  [f"{nl[4]}うええええええん", "", ""]],
                 [[f"{nl[3]}講義棟Cにきたよ！！！陰キャCSには", "無縁の場所だね！", ""], 
                  [f"{nl[0]}何言ってんの！！しーー！", "", ""], 
                  [f"{nl[1]}Cだけに？", "", ""], 
                  [f"{nl[4]}うわーーーーん", "", ""]],
                 [[f"{nl[0]}メディアホールだ！！！", "", "※コード書いてる中の人はここらへんで疲れた"], 
                  [f"{nl[1]}なにいいいいいい！！", "", ""], 
                  [f"{nl[3]}なにかいるんじゃないのおおおお", "", ""]]]
    def __init__(self) -> None:
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 50)
        self.novel_num = 0

        # 表示させる文章のサーフェイスとレクトの初期状態の定義
        self.image = pg.Surface((WIDTH-200, HEIGHT-600))
        pg.draw.rect(self.image, (0,0,0), (0,0,WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT-(HEIGHT/6)
        self.alpha_num = 255
        
    def update(self, screen, map: Map): 
        self.image.set_alpha(self.alpha_num)
        screen.blit(self.image, self.rect)
        
        # 表示させる文章のサーフェイスと文章の定義
        self.image = pg.Surface((WIDTH-200, HEIGHT-600))
        pg.draw.rect(self.image, (0,0,0), (0,0,WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT-(HEIGHT/6)
        # 文章は三段に分けて表示させる
        self.txt0 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][0], 0, (255, 255, 255))
        self.txt1 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][1], 0, (255, 255, 255))
        self.txt2 = self.font.render(self.novel_lst[map.scene_num][self.novel_num][2], 0, (255, 255, 255))
        self.image.blit(self.txt0, [10, 10])
        self.image.blit(self.txt1, [10, 60])
        self.image.blit(self.txt2, [10, 110])
    
    def alpha(self):
        self.alpha_num -= 5 # alpha値を減らす(徐々に透明にさせる)
        

class Map_player:
    """
    プレイヤー表示に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }
    def __init__(self, i) -> None:
        self.image2 = pg.transform.rotozoom(pg.image.load(f"fig/pl{i}_0.png"), 0, 0.4)
        self.rect2 = self.image2.get_rect()
        self.i = i  # iをのちのupdateで使うために定義
        
        # 表示位置の設定
        if i == 0 or i == 1:
            self.rect2.center = WIDTH/2+(100*i), HEIGHT/2  
        else:
            self.rect2.center = WIDTH/2+(100*(i-2))-50, HEIGHT/2+100
        self.speed = 10 #動かすスピードの設定
        
    def update(self, screen, key_lst, all_mode, scene_num, map_mode):
        screen.blit(self.image2, self.rect2)
        sum_mv = [0, 0] # プレイヤーの移動量のリスト
        
        # マップモードが入れない判定の時(2)はプレイヤーを中央に移動
        for h in range(4):
            if map_mode[scene_num][h] == 1:
                if self.i == 0 or self.i == 1:
                    self.rect2.center = WIDTH/2+(100*self.i), HEIGHT/2  
                else:
                    self.rect2.center = WIDTH/2+(100*(self.i-2))-50, HEIGHT/2+100
        
        # 押されたキーによって移動
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                
        # all_mode(まだ敵が倒されていない)時はプレイヤーを中央に移動
        self.rect2.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1]) 
        if all_mode == 1:
            if self.i == 0 or self.i == 1:
                self.rect2.center = WIDTH/2+(100*self.i), HEIGHT/2  
            else:
                self.rect2.center = WIDTH/2+(100*(self.i-2))-50, HEIGHT/2+100
                
class Map_enemy:
    map_enemy = ["fig/tanni.png", "fig/En1.png","fig/En2.png", "fig/En3.png", "fig/En4.png", "fig/En5.png", "fig/En6.png", "fig/En2.png", "fig/En8.png", "fig/tanni.png", "fig/En2.png", "fig/En11.png"]
    me_xy = [(300, 500), (WIDTH*3/4, HEIGHT/2), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500), (300, 500)]
    def __init__(self) -> None:
        pass
        
    def update(self, screen, i):
        if i == 100:
            pass
        else:
            # enemyを描写
            self.image = pg.image.load(__class__.map_enemy[i])
            self.rect = self.image.get_rect()
            self.rect.center = __class__.me_xy[i]
            screen.blit(self.image, self.rect)


#敵のクラス
class Enemys():
    """
    敵に関するクラス
    """
    def __init__(self, en_hp:int, img:str, e_name:str, en_at:tuple):
        """
        敵のSurfaceを生成
        引数 en_hp : 敵のHP
        引数 img ：敵の画像
        引数 e_name：敵の名前
        引数 en_at : 敵の攻撃力
        """
        #敵のHP
        self.en_hp = en_hp
        self.img = img
        #敵の画像パスを引数として指定
        self.image = pg.image.load(img)
        self.image = pg.transform.rotozoom(self.image, 0, 2.5)
        #背景画像
        self.bg_img2 = pg.image.load(f"fig/ending.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, (HEIGHT//2)-150)
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.black = (0, 0, 0)
        self.name = e_name
        #与えた、ダメージ量と攻撃相手を保管
        self.damage = 0
        self.en_at = en_at

    def update(self, screen:pg.Surface):
        """
        敵のHPと画像を画面に表示する
        引数 screen：Surface
        """
        #敵のHPを表示
        self.img2 = self.fonto.render("HP : " + str(self.en_hp), 0 ,self.black)
        screen.blit(self.bg_img2, [0, 0])

        #敵の画像を表示
        screen.blit(self.image, self.rect)
        screen.blit(self.img2, (self.rect.centerx-200, self.rect.y - 35))


#プレイヤーのクラス/HPとMPの表示もここでやってます。
class Player():
    """
    プレイヤーに関するクラス
    """
    def __init__(self, max_hp: int, max_mp: int, pl_hp:int, pl_mp:int, pl_x:int, num:int, name:str):
        """
        プレイヤーのSurfaceを作成
        引数 max_hp：プレイヤーの最大HP
        引数 max_mp：プレイヤーの最大MP
        引数 pl_hp：プレイヤーのHP
        引数 pl_mp：プレイヤーのMP
        引数 pl_x：プレイヤーのｘ座標を指定
        引数 num： プレイヤーの画像を番号で指定
        引数 name：プレイヤーの名前
        """
        self.pl_hp = pl_hp
        self.pl_mp = pl_mp
        self.max_hp = max_hp
        self.max_mp = max_mp
        #番号で画像を指定可能
        self.image = pg.image.load(f"fig/PL{num}.png")
        self.rect = self.image.get_rect()
        #これは無くても可、画像の大きさ調整用
        self.image = pg.transform.rotozoom(self.image, 0, 0.4)

        self.rect.center = (pl_x, 400) 
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
        self.black = (0, 0, 0)
        self.name = name

        #与えた、ダメージ量と攻撃相手を保管
        self.damage = 0
        self.dead = 0

    def update(self, screen:pg.Surface):
        """
        プレイヤーの画像を表示
        引数 screen：Surface
        """
        #color_flag = 名前の色（HPによって表示色を変えています）
        #color_flag2 = HPとMPの文字の色
        color_flag2 = (255,255,255)

        if self.pl_hp > 300:
            color_flag = (0, 192, 0)
        elif 100 < self.pl_hp <= 300:
            color_flag = (255, 225, 32)
        elif 0 < self.pl_hp < 100:
            color_flag = (255, 0, 0)
        else:
            color_flag = (0, 0, 0)
            color_flag2 = (0, 0, 0)
        
        #プレイヤーの名前
        self.img1 = self.fonto.render(str(self.name), 0, color_flag)
        #プレイヤーのHP
        self.img2 = self.fonto.render("HP : "+str(self.pl_hp), 0, color_flag2)
        #プレイヤーのMP
        self.img3 = self.fonto.render("MP : "+str(self.pl_mp), 0, color_flag2)

        #プレイヤーの画像
        screen.blit(self.image, (self.rect.centerx, self.rect.centery-40))

        #HP,MPの白枠
        pg.draw.rect(screen, (255, 255, 255), (self.rect.centerx - 5, self.rect.centery + 195, 180, 200))
        pg.draw.rect(screen, (0, 0, 0), (self.rect.centerx, self.rect.centery + 200, 170, 190))
        
        #プレイヤー名
        screen.blit(self.img1, (self.rect.centerx + 50, self.rect.centery + 205))
        #プレイヤーHP
        screen.blit(self.img2, (self.rect.centerx + 20, self.rect.centery + 235))
        #プレイヤーMP
        screen.blit(self.img3, (self.rect.centerx + 20, self.rect.centery + 305))


#ターン数表示
class Turn:
    """
    ターン数に関するクラス
    """
    def __init__(self, turn:int):
        """
        ターン数に関する変数の指定
        引数 turn :現在のターン数を取得
        """
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 22)
        self.black = (0, 0, 0)
        self.turn = turn
        self.x = 50
        self.y = 50
        #背景の黒の四角形
        self.bg_surface = pg.Surface((380, 180), pg.SRCALPHA)

    def update(self,screen:pg.Surface):
        """
        ターン数を表示する
        引数 screen ： Surface
        """
        self.img = self.fonto.render("現在のターン:" + str(self.turn//2), 0, (255, 255, 255))
        #プレイヤーのターンであれば
        if self.turn % 2 == 0:
            self.img2 = self.fonto.render("プレイヤーの攻撃！", 0, (255, 255, 255))
        #敵のターンであれば
        else:
            self.img2 = self.fonto.render("敵の攻撃！", 0, (255, 255, 255))
        #背景の黒の四角形 
        self.bg_surface.fill((0, 0, 0, 150))
        screen.blit(self.bg_surface, (20, 20))
        #ターン数
        screen.blit(self.img, (self.x-20, self.y))
        #誰の攻撃か
        screen.blit(self.img2, (self.x+150, self.y))


#爆発エフェクト
class Explosion(pg.sprite.Sprite):
    """
    爆発に関するクラス
    """
    def __init__(self, obj: "Player|Enemys", life: int):
        """
        爆弾が爆発するエフェクトを生成する
        引数1 obj：爆発するBombまたは敵機インスタンス
        引数2 life：爆発時間
        """
        super().__init__()
        img = pg.image.load(f"fig/explosion.gif")
        self.imgs = [img, pg.transform.flip(img, 1, 5)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def update(self):
        """
        爆発時間を1減算した爆発経過時間_lifeに応じて爆発画像を切り替えることで
        爆発エフェクトを表現する
        """
        self.life -= 1
        self.image = self.imgs[self.life // 10%2]
        if self.life < 0:
            self.kill()


#武器に関するクラス（いる？）
class Technology():
    """
    攻撃方法に関するクラス
    """
    def __init__(self, num:int, tech_x:int):
        """
        武器のSurfaceを作成
        引数 player：プレイヤーのインスタンス
        引数 num：画像の指定番号
        tech_x : 武器画像のｘ座標
        """
        self.image = pg.image.load(f"fig/TC{num}.png")
        self.image = pg.transform.rotozoom(self.image, 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (tech_x, 500)

    def update(self, screen:pg.Surface):
        """
        武器画像を画面に表示させる
        引数 screen： Surface
        """
        screen.blit(self.image, self.rect.center)


# HPバーを表示するクラス(敵)
class HP_bar:
    """
    HPバーに関するクラス
    """
    def __init__(self, en:Enemys, max_hp:int):
        """
        HPバーの位置を設定
        引数 en：敵のインスタンㇲ
        引数 max_hp：敵のHP
        """
        self.en = en
        self.max_hp = max_hp

        #ここで大きさの指定可能です。
        self.width = 200
        self.height = 25
        self.x = en.rect.x + 100
        self.y = en.rect.y - 35

    def update(self, screen:pg.Surface):
        """
        HPによるバーの色の変更と表示
        引数 screen：Surface
        """
        #HPの背景の白枠
        pg.draw.rect(screen, (64, 64, 64), (self.x -5, self.y -5, self.width + 10, self.height + 10))
        # ダメージ総量を赤にしています。
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # 残りHPを緑にしています。
        new_width = (self.en.en_hp / self.max_hp) * self.width
        pg.draw.rect(screen, (0, 255, 0), (self.x, self.y, new_width, self.height))


#HPバーを表示するクラス（味方）
class Pl_hp_bar:
    """
    プレイヤーのステータスバーに関するクラス
    """
    def __init__(self, player: Player):
        """
        ステータスバーの初期化
        引数 player: プレイヤーのインスタンス
        """
        self.pl = player
        self.font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.black = (0, 0, 0)

    def update(self, screen: pg.Surface):
        """
        HPとMPのステータスバーを描画
        引数 screen : Surface
        """
        # HPバーの色設定
        if self.pl.pl_hp > 300:
            hp_color = (0, 192, 0)
        elif 100 < self.pl.pl_hp <= 300:
            hp_color = (255, 225, 32)
        elif 0 < self.pl.pl_hp <= 100:
            hp_color = (255, 0, 0)
        else:
            hp_color = (0, 0, 0)
        
        # MPバーの色設定(青)
        mp_color = (0, 0, 255)
        # HPとMPバーの背景色(敵と変化を出すため、グレーにしてます。)
        bg_color = (128, 128, 128)
        # HPとMPバーのサイズ
        bar_width = 130
        bar_height = 20
        # 最大HP,MPから残量を％化
        hp_pa = self.pl.pl_hp / self.pl.max_hp
        mp_pa = self.pl.pl_mp / self.pl.max_mp

        # HPバーの位置とサイズ(手動で微調整したため、値を変えないで！)
        pg.draw.rect(screen, (255, 255, 255), (self.pl.rect.centerx + 15, self.pl.rect.centery + 265, 140, 30))
        hp_bar_rect = pg.Rect(self.pl.rect.centerx + 20, self.pl.rect.centery + 270, bar_width, bar_height)
        new_hp_bar_rect = pg.Rect(self.pl.rect.centerx + 20, self.pl.rect.centery + 270, bar_width * hp_pa, bar_height)

        # MPバーの位置とサイズ(手動で微調整したため、値を変えないで！)
        pg.draw.rect(screen, (255, 255, 255), (self.pl.rect.centerx + 15, self.pl.rect.centery + 340, 140, 30))
        mp_bar_rect = pg.Rect(self.pl.rect.centerx + 20, self.pl.rect.centery + 345, bar_width, bar_height)
        new_mp_bar_rect = pg.Rect(self.pl.rect.centerx + 20, self.pl.rect.centery + 345, bar_width * mp_pa, bar_height)

        # HPバー
        pg.draw.rect(screen, bg_color, hp_bar_rect)
        pg.draw.rect(screen, hp_color, new_hp_bar_rect)
        # MPバー
        pg.draw.rect(screen, bg_color, mp_bar_rect)
        pg.draw.rect(screen, mp_color, new_mp_bar_rect)


#プレイヤーのHPのチェック ※ここにゲームオーバー処理が入る予定です
def check_HP(players:list)->int:
    sum = 0
    #pl.dead/ 生きてたら０、死んでたら１
    for player in players:
        sum += player.dead
    #全てのプレイヤーのHPが０になったら
    if sum == 5:
        print("GameOver")
        #ここでモード切替/仮にNormalにしています。
        mode = "Normal"


#ターン数によるダメージ計算とtext表示
def Battle_calc(players:list, en:Enemys, turn:int, exps:Explosion, en_d:int, num:int, random_d:tuple) -> str:
    """
    引数 players：味方のインスタンスのグループ
    引数 en：敵
    引数 turn：ターン数
    引数 exp : 爆発エフェクト
    引数 en_d: 武器によるダメージ量
    引数 random_d：敵の攻撃力
    """

    #プレイヤーのターンであれば
    if turn % 2 == 0:
        #誰が攻撃したか
        pl = players[num]
        if pl.pl_hp <= 0:
            en_d = 0
            text = Display_text(f"{pl.name}はすでに戦える状態ではない", 20, (30, 100), (200, 0, 0))
        
        # MPが10未満の場合
        elif pl.pl_mp < 10:
            en_d = 5
            en.en_hp -= en_d
            text = Display_text(f"素手で殴る！{en.name}に５ダメージ", 20, (30, 100), (200, 0, 0))

        # キーの入力がない場合、en_dが設定されていない場合
        elif en_d == 0:
            en_d = 5
            en.en_hp -= en_d
            text = Display_text("武器が選択されていません。５ダメージ", 20, (30, 100), (200, 0, 0))

        # 通常の攻撃処理
        else:
            # sm = 最小値 bi = 最大値
            sm, bi = en_d
            en_d_n = random.randint(sm, bi)
            pl.pl_mp -= 10
            en.en_hp -= en_d_n
            en.damage = en_d_n
            text = Display_text(f"{en.name}に{en_d_n}のダメージ！", 30, (30, 100), (200, 0, 0))

            # 最大値のときはクリティカル表示
            if en_d_n == bi:
                text = Display_text(f"クリティカル！{en.name}に{en_d_n}のダメージ！", 20, (30, 100), (255, 255, 0))

            exps.add(Explosion(en, 10))
                
    #敵のターンであれば
    else:
        #ダメージ量をランダムで指定
        #mi = 最小値　max = 最大値
        mi, ma = random_d
        damage = random.randint(mi, ma)

        #aimは誰にダメージを与えるか
        #aimsで生きてるプレイヤーを更新
        aims = []
        for pl in players:
            if pl.pl_hp != 0:
                aims.append(pl)
    
        aim = random.choice(aims)
        aim.damage = damage
        aim.pl_hp -= damage
        if aim.pl_hp < 0:
            aim.pl_hp = 0
            aim.dead = 1
        exps.add(Explosion(aim, 10))
        text = Display_text(f"{aim.name}に{damage}のダメージ！", 30, (30, 100), (200, 0, 0))
        if aim.pl_hp <= 0:
            aim.pl_mp = 0
        #最大攻撃量なら
        if damage == ma:
            text = Display_text(f"クリティカル！{aim.name}に{damage}のダメージ！", 20, (30, 100), (255, 255, 0))
    
    return text


#武器選択の矢印
class Display_allow():
    """
    武器選択の矢印に関するクラス
    """
    def __init__(self, pl:Player):
        """
        矢印のSurfaceの作成
        """
        self.pl = pl
        self.image = pg.image.load(f"fig/tns.png")
        self.image = pg.transform.rotozoom(self.image, 0, 0.07)
        self.rect = self.image.get_rect()
        self.rect.centerx = pl.rect.centerx + 40

    def update(self, screen:pg.Surface, num:int):
        """
        矢印を表示
        引数 screen：Surface
        引数 num：選択プレイヤーのインデックス番号＋１
        """
        update_x = num * self.pl.rect.centerx
        screen.blit(self.image, (update_x, HEIGHT//2-100))


#表示する文字を管理
class Display_text():
    """
    画面に表示する文字に関するクラス
    """    
    def __init__(self, font:str, size, xy:tuple=(WIDTH/2-150, HEIGHT/2), color:tuple = (0,0,0))  -> None:
        """
        テキストに関する要素の初期化
        引数 font：表示したい文字
        引数 size：文字のサイズ
        引数 xy：文字の座標
        引数 color：文字の色
        """
        self.image = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", size)
        self.txt = self.image.render(font, True, color)
        self.xy = xy
        
    def update(self, screen:pg.Surface):
        """
        文字を表示する
        引数 screen：Surface
        """
        screen.blit(self.txt, self.xy)
        pg.display.update()
        time.sleep(1)


#敵の名前から、辞書を参照→インスタンスを作成
def create_enemy(en_name:str, enemys:list)->tuple:
    """
    引数 en_name：敵の名前
    引数 enemys：敵のステータスの辞書
    """
    if en_name in enemys:
        e_image, e_hp, en_at = enemys[en_name]
        e_name = en_name
        
        return (e_hp, e_image, e_name, en_at)


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
    def all_blit(self, screen):  #貼り付け系
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
    def blit_1(self, screen):  #あとがき表示
        screen.blit(self.ed_img, [0, 0])
        screen.blit(self.shikaku,(0,0))
        screen.blit(self.image3,self.rect3)
        screen.blit(self.txt2,[WIDTH/10,470])
        screen.blit(self.txt3,[WIDTH/10,550])
        screen.blit(self.txt4,[WIDTH/10,630])
        pg.display.update()
    def blit_2(self, screen):  #「The　End」表示
        screen.blit(self.ed_img, [0, 0])
        screen.blit(self.shikaku,(0,0))
        screen.blit(self.txt1,[WIDTH/5,HEIGHT/3])
        pg.display.update()
    
def Opening(): #Opening画面（仮置き）
    print("opening")

def main():
    global mode_a, mode_aa
    mode_m = "オープニング"    
    pg.display.set_caption("真！こうかとん無双")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    synopsis = Synopsis() #初期値
    map = Map()
    novel = Novel()
    novel_mode = 0
    mpl_lst = []
    for i in range(5):  # プレイヤーごとにクラスの生成
        mpl = Map_player(i)
        mpl_lst.append(mpl)
    all_mode = 0
    Map_Mode = "normal "    # mapモードがonであるかどうか(マージ後の初期値はnormal)
    map_enemy = Map_enemy()
    enemy_mode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    map_mode = [[0, 0, 2, 2], [0, 2, 0, 2], [0, 0, 0, 2], 
                [2, 0, 0, 0], [0, 0, 0, 0], [2, 2, 0, 2], 
                [2, 2, 0, 0], [0, 2, 2, 2], [0, 2, 0, 0], 
                [0, 2, 2, 0], [2, 0, 2, 0], [2, 0, 2, 2]]
    map_saki = [[1, 9, 0, 0], [2, 0, 0, 0], [3, 8, 1, 0], 
                [0, 4, 2, 10], [5, 6, 8, 3], [0, 0, 4, 0], 
                [0, 0, 7, 4], [6, 0, 0, 0], [4, 0, 9, 2], 
                [8, 0, 0, 0], [0, 3, 0, 11], [0, 10, 0, 0]]
    score = 0   # 単位数
    map_pl_mode = 100
    music_t = 0
    
    bg = pg.image.load(f"fig/kena-xga.jpg").convert_alpha()
    bg = pg.transform.scale(bg, (WIDTH,HEIGHT)) 
    shikaku = pg.Surface((WIDTH,HEIGHT))
    shikaku_rect = pg.draw.rect(shikaku,(255,255,255),pg.Rect(0,0,WIDTH,HEIGHT))
    shikaku.set_alpha(128)
    gamemode = "0" #ゲームモードを０に設定する
    op_bgm = load_sound("sound/op_bgm.mp3")
    syp_bgm = load_sound("sound/syp_bgm.mp3")
    map_bgm = load_sound("sound/map_bgm.mp3")
    battle_bgm = load_sound("sound/battle_bgm.mp3")
    panch = load_sound("sound/panch.mp3")
    ed_bgm = load_sound("sound/ed_bgm.mp3")
    gameover = load_sound("sound/gameover.mp3")

    mode = "N"

    #en ： 敵のインスタンス
    en = None
    #exps：爆発エフェクト
    exps = pg.sprite.Group()
    #プレイヤーのステータス
    players_stats = {
        "あきは": [600, 100, 600, 100],  # [最大HP, 最大MP, 現在のHP, 現在のMP]
        "ほのか": [400, 400, 400, 400],
        "こうた": [500, 130, 500, 130],
        "さゆか": [500, 300, 500, 300],
        "せいな": [400, 300, 400, 300]
    }
    #敵のステータス
    enemys = {
        "馬":["fig/En1.png", 100, (10, 20)],#敵の名前：画像パス,HP,（攻撃力）
        "熊":["fig/En2.png", 100, (10, 25)],
        "ハッカー":["fig/En3.png", 120, (20,30)],
        "勉強":["fig/En4.png", 40, (1,10)],
        "ポテト":["fig/En5.png", 60, (20,60)],
        "陽キャ":["fig/En6.png", 70, (20,70)],
        "かつ丼":["fig/En8.png", 60, (20,50)],
        "怪獣":["fig/En11.png", 100, (20,90)],
        "こうかとん":["fig/7.png", 200, (10, 120)]
    }
    #プレイヤーインスタンスの保管場所
    players = []
    #武器のリスト
    techs = []
    #敵のダメージ量
    en_d = 0
    #ターン数の初期設定（無いとエラー出るため）
    turn = None
    #確か、技の番号を初期化してる
    tech_num = 0
    buttle_num = 0
    #プレイヤーのHP,MPバー
    status_bars = []
    #何の敵と遭遇したか。str（敵の名前）
    en_flag = None
    ed_img = pg.image.load(f"fig/ending.png") #Ending用背景
    go = GameOver()
    ed = Ending(ed_img)
    
    while True:
        if mode_a == "マップ":
            mode_m = "マップ"
        if mode_aa == 1:
            music_t = 0
            mode_aa = 0
        if mode_m == "オープニング" and music_t == 0:
             op_bgm.play()
             music_t = 1
        elif mode_m == "あらすじ" and music_t == 0:
            syp_bgm.play()
            music_t = 1
            # if synopsis.num == 0:
                # syp_bgm.fadeout(10)  #フェードアウト
        elif mode_m == "マップ" and music_t == 0:
            map_bgm.play()
        elif mode_m == "バトル" and music_t == 0:
            battle_bgm.play()
            if battle == 1: #攻撃が行われたとき#ループなし
                panch.play()
        elif mode_m == "エンディング" and music_t == 0:
            ed_bgm.play()
        elif mode_m == "ゲームオーバー" and music_t == 0: #ループなし
            gameover.play()
        
        key_lst = pg.key.get_pressed()
        screen.blit(bg_img, [0, 0]) #初期背景貼り付け
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                gamemode = "2"
            if event.type == pg.KEYDOWN and event.key == pg.K_t:
                mode_m = "あらすじ"  #ゲームモードを1にする
                op_bgm.stop()
                music_t = 0
                gamemode = "100"
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                syp_bgm.stop()
                Map_Mode = "map"
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                mode = "Normal"
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if novel_mode == 2:
                    novel_mode = 0
                    novel.alpha_num = 255
                elif novel.novel_num == len(Novel.novel_lst[novel.novel_num])-1:
                    novel_mode = 1
                else:
                    novel.novel_num += 1
            if mode_m == "あらすじ":
                if not synopsis.key_event(event):
                    pg.quit()
                    sys.exit()
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
            mode = "title"

        if mode_m == "あらすじ":
            synopsis.update(screen)
                    
            "＜＜ここからバトル処理＞＞"
            if mode == "Normal":
                if event.type == pg.KEYDOWN:

                    #表示、キー入力にしてあります。
                    if event.key == pg.K_q:
                        en_flag = "馬"
                    elif event.key == pg.K_w:
                        en_flag = "熊"
                        print(en_flag)
                    elif event.key == pg.K_e:
                        en_flag = "ハッカー"
                    elif event.key == pg.K_r:
                        en_flag = "勉強"
                    elif event.key == pg.K_t:
                        en_flag =  "ポテト"
                    elif event.key == pg.K_y:
                        en_flag = "陽キャ"
                    elif event.key == pg.K_u:
                        en_flag = "かつ丼"
                    elif event.key == pg.K_i:
                        en_flag = "怪獣"
                    elif event.key == pg.K_k:
                        en_flag = "こうかとん"

                """<<共通設定>>"""
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    #バトルモードに変更
                    mode = "Battle"
                    #ターン数
                    turn = 0
                    t = Turn(turn) 
                    #武器選択の初期位置
                    flag = 1
                    #敵のステータスをen_flag（敵の名前）によって決めています。
                    enemy_data = create_enemy(en_flag, enemys)
                    if enemy_data:
                        e_hp, e_image, e_name, en_at = enemy_data
                        #敵のインスタンスの作成
                        en = Enemys(e_hp, e_image, e_name, en_at)
                        #敵のHPバーの作成
                        en_hp_bar = HP_bar(en, en.en_hp)


                    """最初のバトルの時は各インスタンスを生成"""
                    if buttle_num == 0:
                        #味方のインスタンスの作成
                        for i, (name, stats) in enumerate(players_stats.items(), start=1):
                            max_hp, max_mp, pl_hp, pl_mp = stats
                            pl_x = 195 * i  # pl_xの計算方法
                            pl = Player(max_hp, max_mp, pl_hp, pl_mp, pl_x, i, name)
                            players.append(pl)
                            status_bars.append(Pl_hp_bar(pl))

                        #武器のインスタンスを作成
                        for j in range(1, 6):
                            tech = Technology(j, 195*j)
                            techs.append(tech)
                        #武器選択の矢印のインスタンス作成
                        allow = Display_allow(players[0])
                        buttle_num = 1
                    else:
                        en.hp = e_hp

                    """が現れた・デバック用です"""
                    start_t = Display_text(f"{e_name}が現れた！",40)
                    start_t.update(screen)

                    
            #バトルモードの時
            if mode == "Battle":
                #キーより武器を選択するための辞書 / 値：（ダメージ量タプル,武器番号）
                en_damages = {
                    pg.K_1: ((1,120), 1),
                    pg.K_2: ((10,30), 2),
                    pg.K_3: ((4,60), 3),
                    pg.K_4: ((10,60), 4),
                    pg.K_5: ((20,50), 5)

                }
                #キーを取得し、武器に応じたダメージ量を返す
                key_lst = pg.key.get_pressed()
                for key, value in en_damages.items():
                    if key_lst[key]:
                        en_d = value[0]
                        tech_num = value[1] -1
                        #武器選択の矢印
                        allow.update(screen, value[1])
                    if not key_lst:
                        en_d = 0
                        
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:  
                        #ターン数に応じて、hpの処理をする
                        text = Battle_calc(players, en, turn, exps, en_d, tech_num, en.en_at)
                        turn += 1
                        t.turn = turn
                        text.update(screen)
                        if check_HP(players):
                            print("GameOver")
                        
                """敵を倒した処理・エンディングへの遷移可能"""
                if en.en_hp <= 0:
                    mode = "Normal"
                    bg_img = pg.image.load(f"fig/ending.png")
                    screen.blit(bg_img, [0, 0])

                    #こうかとんを倒したらエンディングへ
                    if en.name == "こうかとん":
                        mode = "Ending"
                        image = pg.image.load(f"fig/8.png")
                        image = pg.transform.rotozoom(image, 0, 3.0)
                        screen.blit(image, (WIDTH//2, HEIGHT//2 - 200))
                        at_txt = Display_text(f"{en.name}を倒した！", 40)
                        at_txt.update(screen)
                    
                    #共通処理
                    at_txt = Display_text(f"{en.name}を倒した！", 40)
                    at_txt.update(screen)
                    pg.display.update()
                    time.sleep(2)

        if mode == "あらすじ":
            synopsis.update(screen)

        if gamemode == "0": #もしゲームモードが0ならば
            fonto1 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 80)
            img1 = fonto1.render("倒せこうかとん", 0, (0, 0, 0)) #タイトル
            screen.blit(bg,[0,0]) #背景画像
            screen.blit(shikaku, shikaku_rect)
            screen.blit(img1, [400, 150])
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 40)
            img2 = fonto2.render("Press t to Start", 0, (0, 255, 255))
            screen.blit(img2, [450, 400])
            cha1 = pg.image.load(f"fig/PL4.png").convert_alpha()
            cha1 = pg.transform.scale(cha1, (400, 400)) 
            screen.blit(cha1,[-50,400]) #キャラクター1
            cha2 = pg.image.load(f"fig/PL6.png").convert_alpha()
            cha2 = pg.transform.scale(cha2, (400, 400)) 
            screen.blit(cha2,[190,400]) #キャラクター2
            cha3 = pg.image.load(f"fig/PL3.png").convert_alpha()
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
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
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
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha2 = pg.image.load(f"fig/PL6.png").convert_alpha()
            cha2 = pg.transform.scale(cha2, (500, 500)) 
            screen.blit(cha2,[0,200]) #キャラクター2
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
            screen.blit(chara3pro, [400, 400]) #chara3pro表示
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha3 = pg.image.load(f"fig/pl5.png").convert_alpha()
            cha3 = pg.transform.scale(cha3, (500, 500)) 
            screen.blit(cha3,[0,200]) #キャラクター3
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
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha4 = pg.image.load(f"fig/chibi_20240527_185904.png").convert_alpha()
            cha4 = pg.transform.scale(cha4, (500, 500)) 
            screen.blit(cha4,[0,200]) #キャラクター4
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
            fonto2 = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 20)
            chara5pro = fonto2.render("backspaceでオープニング", 0, (0, 0, 0))
            screen.blit(chara5pro, [1000, 600]) #戻り方表示
            cha5 = pg.image.load(f"fig/chibi_20240527_181131.png").convert_alpha()
            cha5 = pg.transform.scale(cha5, (500, 500)) 
            screen.blit(cha5,[0,200]) #キャラクター5
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT: #もしライトキーが押されたら
                    gamemode = "2"
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT: #もしレフトキーが押されたら
                    gamemode = "5"
                if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: #もしバックスペースキーが押されたら
                    gamemode = "100"
                    Map_Mode = "map"
        
        if Map_Mode == "map":
            map.update(screen, score)
            map_pl_mode = 100
            if novel_mode == 1:
                novel.alpha()
                if novel.alpha_num == 0:
                    novel.alpha_num = 0
                    novel.novel_num = 0
                    novel_mode = 2
            novel.update(screen, map)
            
            # mapの画面遷移についてのfor文
            for mpl_k in mpl_lst:
                if check_bound(mpl_k.rect2) != (True, True):
                    if enemy_mode[map.scene_num] == 1:
                        all_mode = 1
                        if map_mode[map.scene_num][0] == 0 and check_bound2(mpl_k.rect2) == (False, True, True, True):
                            map_pl_mode = 0
                        elif map_mode[map.scene_num][1] == 0 and check_bound2(mpl_k.rect2) == (True, False, True, True):
                            map_pl_mode = 1
                        elif map_mode[map.scene_num][2] == 0 and check_bound2(mpl_k.rect2) == (True, True, False, True):
                            map_pl_mode = 2
                        elif map_mode[map.scene_num][3] == 0 and check_bound2(mpl_k.rect2) == (True, True, True, False):
                            map_pl_mode = 3
                    else:
                        all_mode = 1
            
            # 実際の画面変位動作の実行
            if map_pl_mode == 0:
                map.scene_num = map_saki[map.scene_num][0]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 1:
                map.scene_num = map_saki[map.scene_num][1]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 2:
                map.scene_num = map_saki[map.scene_num][2]
                novel.novel_num = 0
                novel.alpha_num = 255
            elif map_pl_mode == 3:
                map.scene_num = map_saki[map.scene_num][3]
                novel.novel_num = 0
                novel.alpha_num = 255
                
            # プレイヤーをupdate
            for mpl_k in mpl_lst:
                mpl_k.update(screen, key_lst, all_mode, map.scene_num, map_mode)
            all_mode = 0    # all_modeをリセット
            map_enemy.update(screen, map.scene_num)
            
            # 敵とプレイヤーが遭遇した時の処理
            for mpl in mpl_lst:
                if map_enemy.rect.colliderect(mpl.rect2):
                    enemy_mode[map.scene_num] = 1
            novel.update(screen, map)

        
        #各要素を画面に表示する
        if mode == "Battle":
            en.update(screen)
            t.update(screen)
            #プレイヤーとプレイヤーのステータスバー
            for pl in players:
                pl.update(screen)
                for status_bar in status_bars:
                    for stats in players_stats.values():
                        status_bar.update(screen)
            #武器の表示
            for te in techs:
                te.update(screen)
            exps.update()
            exps.draw(screen)
            en_hp_bar.update(screen)
            #味方のターンであれば矢印を表示する
            for key, value in en_damages.items():
                if key_lst[key]:
                    flag = value[1]
                    #武器選択の矢印
                if turn % 2 == 0:
                    allow.update(screen, flag)
            
        pg.display.update()   

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()