import pygame as pg
import sys
from random import randint
pg.init()
sf=pg.display.set_mode()
sfrect=sf.get_rect()
wt=pg.Rect(0,0,sfrect.width,10)
wl=pg.Rect(0,0,10,sfrect.height)
wr=pg.Rect(sfrect.width-10,0,10,sfrect.height)

bat=pg.Rect(0,0,200,30)
bat.centerx=sfrect.centerx
bat.centery=sfrect.bottom-200
ball=pg.Rect(bat.centerx-10,bat.top-30,20,20)
retry=pg.Rect(160,1000,370,120)

launch=False
touch=False
rtouch=False
go=0

dx=1
dy=-1
s=1
sr1=8
sr2=12
spdx=10
spdy=10
R=255
G=255
B=255

scfont=pg.font.SysFont('Arial',350)
outfont=pg.font.SysFont('Arial',128)
retryfont=pg.font.SysFont('Arial',100)
hifont=pg.font.SysFont('Arial',50)
clk=pg.time.Clock()

batsound='batsound.wav'
pg.mixer.music.load(batsound)
pg.mixer.init()

while True:
	with open('hiscore.txt','r') as file:
		hi=file.read()
	if s>int(hi):	
		with open('hiscore.txt','w') as file:
			file.write(str(s))
	sclabel=scfont.render(f'{int(s/100)}{int(s/10)}{s%10}',1,(200,255,230))
	outlabel=outfont.render('Game Over',0,(255,0,0))
	retrylabel=retryfont.render('RETRY',0,(255,255,255))
	hilabel=hifont.render(f'HI-SCORE={hi}',0,(255,240,150))
	for ev in pg.event.get():
		if ev.type==pg.QUIT:
			sys.exit()
		if ev.type==pg.MOUSEBUTTONDOWN:
			#if bat.collidepoint(ev.pos):
			touch=True
			launch=True
			if retry.collidepoint(ev.pos):
				rtouch=True	
				go=0
				pg.mixer.music.load('batsound.wav')
		if ev.type==pg.MOUSEBUTTONUP:
			touch=False
	if launch:
		ball=ball.move(spdx*dx,spdy*dy)
		if ball.left<wl.right+10:
			dx=1
			pg.mixer.music.play()
		if ball.right>wr.left-10:
			dx=-1
			pg.mixer.music.play()
		if ball.top<wt.bottom+10:
			dy=1
			pg.mixer.music.play()
		if ball.bottom>bat.top and ball.bottom<bat.centery and ball.centerx>bat.left and ball.centerx<bat.right:
			dy=-1
			s+=1
			spdx+=1
			spdy+=1
			R=255
			G=255
			B=255
			pg.mixer.music.play()
		if ball.bottom>bat.bottom+210:
			dx=0
			dy=0	
	if touch:
		bat.move_ip(pg.mouse.get_rel())
		bat.centery=sfrect.bottom-200
		bat.clamp_ip(sfrect)
	if rtouch:
		launch=False
		dx=-1
		dy=-1
		s=1
		spdx=10
		spdy=10
		bat.centerx=sfrect.centerx
		bat.centery=sfrect.bottom-200
		ball.bottom=bat.top-10
		ball.centerx=bat.centerx
		rtouch=False
	sf.fill((0,0,0))	
	pg.draw.rect(sf,(250,250,250),wt)
	pg.draw.rect(sf,(250,250,250),wl)
	pg.draw.rect(sf,(250,250,250),wr)
	sf.blit(sclabel,(70,200))
	sf.blit(hilabel,(230,10))
	if ball.bottom>sfrect.bottom:
		sf.blit(outlabel,(50,650))
		pg.draw.rect(sf,(140,140,140),retry)
		sf.blit(retrylabel,(200,1000))
		go+=1
		if  go==1:
			pg.mixer.music.load('gameover.wav')
			pg.mixer.music.play()
	#pg.draw.circle(sf,(0,0,0),(ball.centerx,ball.centery),22)		
	pg.draw.rect(sf,(250,250,250),bat)
	pg.draw.circle(sf,(R,G,B),(ball.centerx,ball.centery),20)
	
	clk.tick(50)
	pg.display.flip()
