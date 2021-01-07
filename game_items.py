import  pygame
import random

# 背景颜色
bg_color=(232,232,232)
#分数字体颜色
SCORE_TEXT_COLOR = (192,192,192)
#提示字体颜色
TIP_TEXT_COLOR = (64,64,64)
SCREEN_RECT = pygame.Rect(0,0,640,480)

CELL_SIZE = 20

FOOD_UPDATE_EVENT = pygame.USEREVENT # 食物跟新标志
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1







class Label(object):
    def __init__(self,size=32,is_score=True):
        '''初始化标签信息
        :pararm size
        '''
        self.font=pygame.font.SysFont('simhei',size)
        self.is_score = is_score

    def draw(self,window,text):
        #绘制对象的内容

        #渲染字体
        color=SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        text_surface=self.font.render(text,True,color)

        #获取文本的矩形
        text_rect = text_surface.get_rect()
        #获取窗口的巨型
        window_rect = window.get_rect()

        #修改显示的坐标
        if self.is_score:
            # text_rect.y=window_rect.height - text_rect.height
            #修改label右下脚和windowbuootmleft一致就可以对齐。
            text_rect.bottomleft=window_rect.bottomleft
        else:
            #其他提示信息：比如暂停等显示在画面中央
            text_rect.center = window_rect.center


        #绘制渲染结果 blit
        window.blit(text_surface,text_rect)


class Food:
    def __init__(self):
        self.color = (255,0,0,0) #初始失误颜色
        self.socre = 10
        self.rect = (0,0,CELL_SIZE,CELL_SIZE) #初始显示位置

    # 初始化食物是随机分配一个位置
        self.randow_rect()




    def draw(self,window):
        if self.rect.w < CELL_SIZE: # 只要显示的矩形小于单元格，就逐渐放大
            self.rect.inflate_ip(2,2)

        pygame.draw.ellipse(window,self.color,self.rect)

    def randow_rect(self):
        #结束可用的行数和列数
        SCREEN_RECT_W = 640
        SCREEN_RECT_H = 480

        col = SCREEN_RECT.w/CELL_SIZE -1 #列
        row = SCREEN_RECT.h/CELL_SIZE -1 #行

        x = random.randint(0,col) * CELL_SIZE
        y = random.randint(0,row) * CELL_SIZE

        self.rect = pygame.Rect(x , y, CELL_SIZE,CELL_SIZE)
        self.rect.inflate_ip(-CELL_SIZE,-CELL_SIZE) # 把创建的圆还原为大小为0

        # 时间到了，重行更新食物位置
        pygame.time.set_timer(FOOD_UPDATE_EVENT,30000)


class Snake():
    def __init__(self):
        self.dir = pygame.K_RIGHT  #默认运动方向
        self.time_interval = 500 #运动速度
        self.score = 0  #启动得分
        self.color = (64,64,64) #身体颜色、深灰色
        self.body_list = [] #身体列表
        self.reset_snake()  # 重置蛇的数据，包含3节身体




    def reset_snake(self):
        #重置蛇的数据
        self.dir = pygame.K_RIGHT
        self.time_interval = 500
        self.score =0
        self.body_list.clear()

        for _ in range(3):
            self.add_node()

    def add_node(self):
        #添加一节身体
        if self.body_list:
            #已有身体
            head = self.body_list[0].copy()

        else:
            #没有身体
            head= pygame.Rect(-CELL_SIZE,0,CELL_SIZE,CELL_SIZE)

        #根据移动反向，把新生成的头部放到恰当的位置。
        if self.dir == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.dir == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif  self.dir == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:
            head.y += CELL_SIZE

        #把新生成的头部放到列表的最前面
        self.body_list.insert(0,head)

        # 定时跟新snake
        pygame.time.set_timer(SNAKE_UPDATE_EVENT,self.time_interval)

    def draw(self,window):
        # 绘制蛇的每一节身体
        for indx , rect in enumerate(self.body_list):
            pygame.draw.rect(window , self.color,rect.inflate(-2,-2),indx == 0)
    def updat(self):
        # 移动蛇的身体

        #备份移动之前的身体列表
        body_list_copy = self.body_list.copy()


        #添加head ，然后把末尾删除，判断是否身体死亡，如果死亡，身体恢复到异动前状态并停止。
        self.add_node()
        self.body_list.pop()


        #判断是否死亡
        if self.is_dead():
            self.body_list = body_list_copy
            # print('yidongshibai')
            return False
        return True



    def change_dir(self,to_dir):
        """修改蛇的移动方向"""
        hor_dir = (pygame.K_LEFT,pygame.K_RIGHT) #水平方向
        ver_dir = (pygame.K_DOWN,pygame.K_UP) #垂直方向
        #判断能否移动

        print(self.dir,to_dir)
        if (self.dir in ver_dir and to_dir not in ver_dir) or (self.dir in hor_dir and to_dir not in hor_dir):

            self.dir = to_dir

    def has_food(self,food):
        """判断是吃到食物"""
        if self.body_list[0].contains(food.rect):
            self.score += food.socre #修改得分
            #修改蛇的速度
            if self.time_interval >100:
                self.time_interval -= 50
                print(self.time_interval)
            self.add_node()
            return True
        return False

    def is_dead(self):
        '''判断是否出界或者碰到自己的身体'''
        head = self.body_list[0]

        #判断蛇头是否在窗口内
        if not SCREEN_RECT.contains(head):

            return True

        #判断蛇头是否与身体重叠

        for body in self.body_list[1:]:
            if head.contains(body):
                print('12')
                return True

        return False





