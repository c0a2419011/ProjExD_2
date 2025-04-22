import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP :(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    #引数　こうかとんrectまたは爆弾rect
    #戻り値:判定結果タプル(横、縦)
    #画面内ならTrue，画面外ならFalse
    yoko,tate=True,True #横方向、縦方向の判定
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:#画面外だったら
        yoko=False
        #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:#画面内だったら
        tate =False
    return (yoko,tate)


def gameover(screen: pg.Surface) -> None:#ゲームオーバー画面
    black_img= pg.Surface((1100, 650))#黒い画面
    pg.draw.rect(black_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    kk_img2 = pg.image.load("fig/8.png")#泣いてるこうかとん
    fonto = pg.font.Font(None, 40)
    txt = fonto.render("Game Over", True, (255, 255, 255))#gameoverの文字
    black_img.set_alpha(200)#半透明
    screen.blit(black_img,[0,0])
    screen.blit(txt,[550,325])
    screen.blit(kk_img2,[500,325])
    screen.blit(kk_img2,[700,325])
    pg.display.update()
    time.sleep(5)
    
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大，加速する関数
    戻り値 速度のリスト、大きい爆弾
    引数なし
    """
    bmb_lst=[]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0,0,0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bmb_lst.append(bb_img)#大きくなる爆弾
    bb_accs = [a for a in range(1, 11)]#速度リスト
    return bmb_lst,bb_accs 
# def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
  
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    #爆弾初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    vx,vy=+5,+5
    
      
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        # screen.blit(kk_img2,)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            # time.sleep(5)
            
            return
        # if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が重なっていたら
        #     screen.blit(black_img,[0,0])
        #     time.sleep(5)
        #     return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]#合計移動量リスト 
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #左右方向
                sum_mv[1] += mv[1] #上下方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)#こうかとんの移動
        if check_bound(kk_rct) != (True,True):#画面の外だったら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_img = bb_imgs[min(tmr//500, 9)]
        avx = vx*bb_accs[min(tmr//500, 9)]#横速度
        avy = vy*bb_accs[min(tmr//500, 9)]#縦速度
        
        # kk_img = get_kk_img((0, 0)) 
        # kk_img = get_kk_img(tuple(sum_mv))

        bb_rct.move_ip(avx,avy)#爆弾の移動
        yoko,tate = check_bound(bb_rct)
        if not yoko:#左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:
            vy *= -1
                        
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
