import pygame

from game_items import *


class Game(object):
    def __init__(self):
        self.main_window=pygame.display.set_mode((640,480))
        pygame.display.set_caption("贪吃蛇")
        #等分的标签
        self.score_label=Label()
        # self.score = 0
        self.is_game_over = False #游戏是否结束标记
        self.is_pause = False #游戏是否暂停
        self.tip_label = Label(24,False)  #暂停\结束标签
        self.food = Food()
        self.snake =Snake()

        # print(self.snake.body_list)





    def start(self):
        #启动游戏
        clock=pygame.time.Clock()  #游戏时钟
        while True:
            #事件监听
             #退出判断
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type ==  pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset_game()
                        else:
                            self.is_pause = not self.is_pause
                # 定时更行食物图形
                if not self.is_pause and not self.is_game_over:
                    if event.type == FOOD_UPDATE_EVENT:
                        self.food.randow_rect()
                    elif event.type == SNAKE_UPDATE_EVENT:

                        self.is_game_over = not self.snake.updat()

                    elif event.type == pygame.KEYDOWN:
                        # 有键盘按下，判断方向
                        print(event.key in (pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN))
                        if event.key in (pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN):
                            self.snake.change_dir(event.key)



            self.main_window.fill(bg_color)
            #绘制得分

            self.score_label.draw(self.main_window,'得分：%d' % self.snake.score)

            #绘制暂停 有戏结束的标签
            if self.is_game_over:
                self.tip_label.draw(self.main_window, "游戏结束。。。。")

            elif self.is_pause :
                self.tip_label.draw(self.main_window, "游戏暂停，空格键继续。。。。")
            else:
                if self.snake.has_food(self.food):
                    self.food.randow_rect()



            #绘制食物
            self.food.draw(self.main_window)

            #绘制贪吃蛇
            self.snake.draw(self.main_window)

            #更新窗口颜色
            pygame.display.update()
            #设置刷新率
            clock.tick(60)

    def reset_game(self):
        '''重置有戏'''
        self.score = 0
        self.is_game_over = False
        self.is_pause = False

        #重置蛇的数据
        self.snake.reset_snake()


        #重置食物数据
        self.food.randow_rect()




#游戏开始初始化pygame模块
if __name__=='__main__':

    # print("jj")
    pygame.init()
    Game().start()





    #pygame.quit()
