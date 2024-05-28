import os
import time
import pygame as pg
import random
import sys


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1280, 800


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


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"fig/ending.png")
    mode = "Normal"

    """<<共通の変数>>"""
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


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

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

                    #敵のステータスをen_flag（敵の名前）によって決めています。
                    enemy_data = create_enemy(en_flag, enemys)
                    if enemy_data:
                        e_hp, e_image, e_name, en_at = enemy_data
                        #敵のインスタンスの作成
                        en = Enemys(e_hp, e_image, e_name, en_at)
                        #敵のHPバーの作成
                        en_hp_bar = HP_bar(en, en.en_hp)

                """<<共通設定>>"""
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    #バトルモードに変更
                    mode = "Battle"
                    #ターン数
                    turn = 0
                    t = Turn(turn) 
                    #武器選択の初期位置
                    flag = 1

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
        
        #起動直後の背景の表示（エラーが出る場合は消して大丈夫です。）
        screen.blit(bg_img, [0, 0])
        
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