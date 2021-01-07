### 4.游戏框架搭建

在这一小节，重点给大家介绍一下使用pygame开发图形界面游戏的几个要素，并且把贪吃蛇游戏的整体框架搭建完成。

本小节的知识重点包括：

[toc]

1. pygame的初始化和退出
2. 游戏主窗口
3. 游戏循环和游戏时钟
4. 主窗口背景颜色
5. 绘制文本
6. pygame的坐标系
7. 游戏事件监听
8. 绘制图形
9. 定时器事件





#### 4.1pygame的初始化和退出

在之前小节中已经介绍过— pygame是专为开发电子游戏而设计的跨平台的 Python包。而包中又针对不同的开发需求提供有不同的模块,例如:显示模块、宁体模块、混音器模块等等。

> 注意:在这些模块中,有部分模块是必须要初始化之后,才能够正常使用的,例如:宁体模块等。
pygame为了程序员更加方便地使用包中的模块,提供有两个方法——init和quit,其中

- init方法可以一次性初始化 pygame的所有模块,这样在后续开发中,程序员可以直接使用这些模块而不必再单独为某一个模块调用对应的初始化方法
- quit方法可以取消初始化之前已经初始化过的模块
  - 提示,由于 Python解释器在退出之前会释放所有的模块,所以quit方法不是必须要调用的。

要实现  pygame的初始化和退出,需要在game,py模块中实现以下代码

```python
import pygame#导入 pygame
from game_items import *#导入游戏元素模块中的所有类和全局变量
if __name__ == '__main__'

pygame.init()#初始化所有模块
#游戏代码
pygame.quit()#取消初始化所有模块
```

>提示：虽然quit方法的调用不是必须的，但是很多程序员在开发程序时，还是习惯按照谁申请、谁释
>放的原则来编写代码。因此，大家可以在很多pygame的开源代码中看到init和quit成对调用的情
>况。

**阶段性小结 **

- pygame针对不同的开发需求提供有不同的模块
- 为了保证顺利地使用每一个模块，在程序开始之前调用一下pygame.init()是个不错的选择！

#### 4.2 游戏主窗口



**贪吃蛇**游戏是一款**图形界面游戏**，而所谓的图形界面就是指一程序启动时，首先应该呈现一个图形化的
窗口，所有游戏元素（例如**：蛇、食物、得分**等）都显示在这个窗口的内部。
pygame的**display**模块提供的一系列方法可以用于创建游戏窗口以及更新窗口显示内容等操作。常用方法
如下：

| 序号 | 方法                         | 备注                       |
| ---- | ---------------------------- | -------------------------- |
| 1    | pygame.display.set_mode()    | 初始化游戏                 |
| 2    | pygame.dispaly.set_caption() | 设置窗口标题               |
| 3    | pygame.display.update()      | 更新屏幕显示内容，稍后介绍 |

##### 4.2.1 创建游戏主窗口方法

使用set_mode方法，可以非常方便地创建一个游戏主窗口，语法格式如下：

```python
set_mode(resolution = (0,0),flags = 0 ,depth = 0) ->Surface
```


其中：

- 参数
  - resolution指定屏幕的宽和高的元组，默认创建的窗口大小和屏幕大小一致
  - flags参数指定屏幕的附加选项，例如是否全屏等等，默认使用resolution指定的窗口大小
  - depth参数表示颜色的位数，默认自动匹配
- 返回
  - Surface对象
    - 可以把一个Suface对象被看作是一个油画的画布，我们可以在这个画布上作画，例如：绘制
      贪吃蛇、绘制食物、绘制分数文字等
    - 所有游戏元素绘制在游戏的主窗口之后，就是用户看到的游戏画面

> 注意：必须记录set_mode方法的返回结果！因为后续其他的游戏元素都需要绘制在游戏主窗口上。

<img src="https://i.loli.net/2021/01/06/6xJVyeDUdo8hPpA.png" alt="image-20201227212153599" style="zoom: 80%;" />

<img src="https://i.loli.net/2021/01/06/CqRSBpkxGEsQnur.png" alt="image-20201227212225098" style="zoom:80%;" />





#### 4.3游戏循环和游戏时钟

##### 4.3.1游戏循环

要做到游戏程序启动执行之后，不会立即退出，需要在游戏程序中增加一个游戏循环。所谓游戏循环就是一个无限循环。

要想让贪吃蛇游戏启动执行之后，不会立即退出，可以在Game类中增加start方法，并且实现如下代码：

![image-20201227212613571](https://i.loli.net/2021/01/06/58vgRo3aQWxFTbV.png)

##### 4.3.2 游戏中的动画实现原理

在一款图形界面的游戏中，通常游戏的画面是不断变化的，也就是我们常说的动画。例如：贪吃蛇的运动、食物的出现与消失以及分数值的变化等等。
那么游戏中的动画效果是怎样实现的呢？跟电影的原理类似，游戏中的动画效果，本质上是快速地在屏幕上绘制图像。

- 电影是将多张静止的电影胶片连续、快速地播放，产生连贯的视觉效果！
- 一般在电脑上每秒绘制60次，就能够达到非常连续、高品质的动画效果
  - 每次绘制的结果被称为帧Frame

因此，在我们刚刚完成的代码中，无限循环的执行频率（刷新帧率）只要能达到每秒60帧，就能够达到我们预期的动画效果了。但是，实际运行中，这个无限循环的执行频率有多快呢？

我们先调整一下start方法中的代码，运行观察一下循环体的执行频率，代码如下：

```python
i = 0
while True
	print(i)
	i += 1
```

运行程序会发现循环体的执行频率非常高！远远超过了我们预期的60帧秒，而且CPU的负荷也比较大。

##### 4.3.3 游戏时钟



pygame的time模块中专门提供了一个Clock类，可以非常方便地设置游戏循环的执行频率——刷新帧
率。

> 以60帧/秒举例，当循环体代码执行一遍之后，我们让程序休息1/60秒，然后再次执行循环体代码，
> 这样就能够做到循环体内部的代码，每秒只会被执行60次了，同时CPU的负荷也能够大大降低。

要设置刷新帧率需要2个步骤：
1.在游戏循环的循环体上方创建一个时钟对象
2.在游戏循环的循环体的末尾让时钟对象调用tick(帧率）方法来设置刷新帧率

- 提示：tick方法会根据上次被调用的时间，自动设置游戏循环中的延时,要想设置刷新帧率，可以对start方法的代码调整如下：

```python
def start(self):
	clock = pygame.time.Clock()
	
    i = 0
    while True:
        print(i)
        
        i+=1
        
        clock.tick(60)
```

4.4  主窗口背景颜色

4.4.1 pygame 的颜色定义

pygame的颜色使用的是RGB色彩模式，即通过对红（R)、绿（G)、蓝（B)三个颜色相互之间的叠加来得到各种各样的颜色。

在pygame中，使用一个（R,G,B)格式的元组来定义一个颜色，其中，红（R)、绿（G)、蓝（B)的数值是
0~255之间的一个整数。数值对应颜色的亮级，数值越大亮级就越大。

4.4.2 定义并绘制窗口背景颜色

首先，在game_item.py模块中定义一个主窗口背景颜色的全局常量，代码如下：

```
import pygame
#全局变量定义
BACKGROUND COLOR = (232, 232, 232)
```



#主窗口背景颜色
提示：

- Python中没有变量和常量的区别
  - 所谓常量就是定义之后，只允许访问，但是不允许修改
- Python中，如果要定义常量，可以使用全大写命名，单词之间使用_分隔
  然后，修改Game类的start方法，填充窗口颜色并更新显示，代码如下：

![image-20201227214605466](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201227214605466.png)

#### 4.5绘制文本

pygame的font模块中专门提供了一个SysFont类，可以创建系统字体对象，从而能够实现在游戏窗口中绘制文字内容。

要想在游戏窗口中绘制文本内容，需要执行以下3个步骤：

1.创建字体对象
2.用字体渲染指定的文本内容，并生成一张图像（Surface对象）
3.将生成的图像绘制在游戏主窗口的指定位置

以上三个步骤的示意图如下：
![image-20201227214754676](https://i.loli.net/2021/01/06/rWMi2bN8wkuaTLs.png)

##### 4.5.1创建字体对象

SysFont的初始化方法的语法如下：

```python
SysFont(name,size,bold=false,italic=False) ->Font
```

其中：

- 参数
  - name系统字体的名称
    - 注意：可以设置的字体与操作系统有关，通过pygame.font.get_fonts()可以获取当前系统
      的所有可用字体列表
  - size字体大小
  - bold是否粗体，默认为否
  - italic是否斜体，默认为否
- ·返回
  - Font对象

代码实现
观察备课代码的运行效果，可以发现贪吃蛇游戏中的文字一共有2种颜色，分别是：
1.分数文字颜色——浅灰色
2.游戏暂停和结束时的提示文字颜色——深灰色

为了方便后续代码的编写，我们首先在game_item.py模块的顶部先定义两个字体颜色常量，代码如下：

![image-20201227221812889](https://i.loli.net/2021/01/06/qvxpPE1SOJyusDG.png)

##### 4.5.2渲染文本内容

使用创建的字体对象调用render方法，渲染生成一张图像（Suface对象）,语法如下：

``` 
render(text,antialias,color,background=None)->Surface

```

其中：

- 参数
  - text文字内容
  - antialias是否抗锯齿，抗锯齿效果会让绘制的文字看起来更加平滑
  - color文字颜色
  - background 背景颜色，默认为None
- 返回
- Surface对象，可以理解为一张刚好包含文字内容的图像
- Surface对象调用get_rect方法，可以获得图像大小



##### 4.5.3绘制渲染结果

pygame为Surface对象提供了一个blit方法，可以在一个Surface对象中绘制另外一个Surface对象的内容。语法如下：

pygame为Surface对象提供了一个blit方法，可以在一个Surface对象中绘制另外一个Surface对象
的内容。语法如下：

```
blit(source,dest,area=None,special_flags=0)->Rect
```

其中：

- 参数
  - source要绘制的图像（Surface对象）
  - dest目标位置
    - 暂时传入（0,0),有关内容在后续小节介绍
- 返回
  - Rect对象，绘制结果对应的矩形区域，有关内容在后续小节介绍

代码实现

- 在Label类中定义draw方法，并接收游戏主窗口作为参数，代码如下：

![image-20201227222332522](https://i.loli.net/2021/01/06/zE9ljZFAYPd7T2K.png)

4.5.4

![image-20201227222518882](https://i.loli.net/2021/01/06/VIoey6kc9jANUCs.png)

>提示：如果大家运行修改后的代码，会发现大约5~10秒之后，游戏分数就不再更新了。先不要着急，这个问题在介绍完游戏坐标系之后就讲。

##### 4.5.5 总结

![image-20201227222654890](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201227222654890.png)

#### 4.6 [pygame的继承](https://www.bilibili.com/video/BV1Dc411h7pd?p=20)

在上一小节，我们把游戏得分的文字绘制在了屏幕的左上角。那如果想要把文字绘制到屏幕的其他位置，应该怎么做呢？

要解决这个问题，首先需要给大家介绍一下pygame的坐标系。

##### 4.6.1 pygame的坐标系

坐标系的用处就是以坐标原点为参照，准确地描述出屏幕上的任意位置或者区域。
1.坐标原点在游戏主窗口的左上角
2.x轴沿水平方向向右，逐渐增加
3.y轴沿垂直方向向下，逐渐增加
![image-20201227222919683](https://i.loli.net/2021/01/06/XhAIajctCoST38d.png)

##### 4.6.2 矩形区域

在游戏中，所有可见的元素都是以矩形区域来描述位置区域的，一个矩形区域包含四个要素：`(x,y）（width,	height)`。

pygame专门提供了一个类Rect用于描述矩形区域，Rect的初始化方法的语法如下：

```d
Rect(x,y,width,height)->Rect
```

知道了矩形区域这个概念之后，接下来我们就做一个实战演练，将得分文字绘制在游戏窗口的左下角。

要实现这一目标，一共需要3个步骤：

1.利用get_rect获得渲染完成的文本图像（Surface对象）的矩形区域
2.通过计算设置文本图像的显示位置
3.利用Rect提供的属性设置文本图像的显示位置
1)获得文本图像的矩形区域

修改Label类的draw方法代码如下：



介绍了Rect的属性之后，现在我们使用属性来修改一下Label类的draw方法，大家可以对比一下修改前后的代码，修改后的代码如下：

![image-20201227223427421](https://i.loli.net/2021/01/06/tASpOMUjQi9wxFa.png)

##### 4.6.3 阶段性小结

- pygame的坐标原点在窗口的左上角，X水平向右递增，y垂直向下递增利用Rect对象可以准确地指定游戏窗口上的某一块矩形区域
  - 合理利用Rect提供的属性，在设置矩形区域时会更加方便

#### 4.7 游戏实践监听

通过之前小节的学习，我们已经知道，游戏循环的主要目的是保证游戏不会立即退出！
除此之外，我们还学习了在游戏循环中，需要做的3件事情，分别是：
1.绘制游戏元素

- 每一次执行游戏循环内的代码，游戏窗口中的所有内容都会被重新绘制

2.更新显示

- 只有调用了pygame.display.update()方法，才能在游戏窗口中看到最终的绘制结果

3.设置刷新帧率

- 达到流畅的动画效果
- 降低CPU负荷

在这一小节，我们要重点学习一下，在游戏循环中要需要做的最后一件事情——事件监听！

##### 4.7.1事件和监听概念

首先，我们来明确2个概念：事件和监听：

- 事件就是游戏启动后，用户针对游戏所做的操作，例如：点击关闭按钮，点击鼠标，按下键盘等
- 监听就是在游戏循环中，判断用户在当前这一时刻，所做的具体操作
- ![](https://i.loli.net/2021/01/06/Q5EHS4RBgJi73xN.png)

##### 4.7.2 pygame 监听事件

pygame专门提供了一个event模块用于处理游戏事件。通过pygame.event.get()方法可以获得当前这一时刻发生的所有事件列表。

> 提示：同一时刻，可能会发生很多事件！例如：在用户按下方向键修改贪吃蛇方向的同时，定时器事件被触发了，此时还需要让贪吃蛇向前移动。

我们首先演练一下对退出事件的监听和处理。找到Game类的start方法，对代码调整如下：

```python
def start(self):
"""开始贪吃蛇游戏"""
	clock=pygame.time.clock()#游戏时钟
 
	while True:
		#事件监听
		for event in pygame.event.get():#遍历同一时刻发生的事件列表
		if event.type==pygame.QUIT:#判断退出事件
		return
		#依次绘制游戏元素
		self.main_window.fill(BACKGROUND_COLOR)
```

紧接着，我们再来监听一下用户按键事件，就是按下ESC键时同样能够直接退出游戏。对start方法的代码调整



##### 4.7.3 游戏状态切换和提示

按照贪吃蛇的游戏规则描述，空格键可以改变游戏的状态：

1.一局游戏结束后，按下空格键可以重新开启一局新游戏
2.游戏过程中按下空格键，可以暂停游戏；再次按下空格键，可以继续游戏
要实现游戏状态的切换，我们分两步来完成：

1.创建提示标签及游戏状态标记，游戏状态不同显示不同的提示信息
2.监听空格键按键，并根据当前游戏状态标记，修改游戏状态

1)提示标签和状态标记

修改Game类的初始化方法，创建提示标签和游戏状态标记，代码如下：



```python
def_init_(self):
    self.main_window=pygame.display.set_mode((640,480))
    pygame.display.set_caption("贪吃蛇")
    self.score=0#游戏得分
    self.score_label=Label()#得分文本标签
    self.tip_label=Label(24,False)#提示标签
    self.is_game_over=False#游戏结束标记
    self.is_pause=False#游戏暂停标记
```

4.7.4 阶段性小结

- 游戏循环中需要做4件事情：

  - 事件监听
  - 绘制游戏元素
  - 更新显示
  - 设置刷新帧率

- 在同一时刻，可能会发生多个事件，因此应该使用`for`来遍历事件列表

- 使用`event.type`可以判断事件的类型，如：退出事件、按键事件等

- 如果是按键事件，使用`event.key`可以判断具体的按键

- #### 4.8绘制图形

  pygame的draw模块中专门提供了一系列方法，可以方便地绘制图形。常用的绘制图形方法如下：

  

| 序号 | 语法                                                     | 说明                             |
| :--- | -------------------------------------------------------- | -------------------------------- |
| 01   | `rect(Surface,color,Rect,width = 0 ) ->Rect`             | 绘制矩形，width>0则绘制边框      |
| 02   | `ellispse(Surface,color,Rect,width = 0 ) ->Rect`         | 绘制与Rect内切的桐圆，width同上  |
| 03   | `ine(Surface,color,start_pos,end_pos,width =1 ) ->Rect`  | 绘制从start_pos到end_pos的线条   |
| 04   | `lines(Surface,color,closed,pointlist,width =1 ) ->Rect` | 绘制多个线条，closed设置首尾相连 |





在这一小节，我们就利用draw模块提供的ellipse方法实现食物的绘制工作。

要实现这一目标，一共需要3个步骤：

1.在屏幕的左上角绘制一个圆形表示食物
2.让食物随机出现
3.增加食物出场动画



##### 4.8.1  简单绘制食物

首先，在game_item.py模块中定义屏幕矩形区域和小格子大小的全局常量，之所以要定义全局常量是因为：

1. 定义屏幕矩形区域是为了方便后续计算食物的位置以及蛇身体的位置
2. 在贪吃蛇游戏中，我们可以把屏幕矩形区域划分成若干个小格子
3. 每一个小格子中，可以显示一个食物或者一节蛇的身体

定义全局常量的代码如下：

```python
# 全局变量定义
SCREEN_RECT = pygame.Rect(0,0,640,480)#游戏窗口矩形区域
CELL_SIZE = 20 #小格子大小
```

在game_item.py模块的末尾，定义Food类，并实现如下代码

```python

```

##### 4.8.2 随机食物位置

在game_item.py模块的顶部，导入random模块，以方便使用随机数

```
import random

```
在Food类中定义random_rect 方法，随机确定游戏窗口的任一小格子设置食物出现的位置，代码如下：
```python
def_init_(self):
    self.color-(255,0,0)#食物颜色-红色
    self.score-10#每颗食物得分10分
    self.rect=self.pygame.Rect(0,0,CELL_SIZE,CELL_SIZE)#食物位置
    self.random_rect()#设置食物随机位置
    
def random(self):
    col = SCREEN_RECT.W/CELL_SIZE-1#屏幕上小格子的列数
    row = SCREEN_RECT.h/CELL_SIZE-1#屏幕上小格子的行数
    x = random.randint(e,col)*CELL_SIZE
    y = random.randint(e,row)*CELL_SIZE
	self.rect-pygane.Rect(x,y,CELL_SIZE,CELL_SIZE)
```

修改Game类的reset_game方法，在游戏复位时，重新设置食物的位置，代码如下：

```python
def reset_game(self):
    pass
	```详见代码```
    


```

##### 4.8.3	食物出现动画

通过之前小节的学习，我们已经知道，游戏循环体中的代码执行频率是每秒60赖，这样做的目的之一是为了达到非常连续、高品质的动画效果。

在实际开发中，我们只需要让连续赖绘制的结果相差不大，这样就能够在视觉上产生连续的动画效果了，如下图所示：
![image-20201228082807765](https://i.loli.net/2021/01/06/CcxmVU6FlH58Ofi.png)

**pygame**在**Rect**类中提供了2个方法**inflate和inflate_ip,**可以非常方便地实现食物由小变大的动画效果，语法如下：

```
inflate(x,y) -> Rect
inflate_up(x,y) -> Rect
```

**inflate**和**inflate_ip**方法都可以**以矩形区域的中心点**为中心，向四周扩大或缩小，其中：

- x表示水平方向缩放的像素，正数放大，负数缩小
- y表示垂百方向缩放的像素，正数放大，负数缩小

> 注意：x和y必须要是偶数，例如传入-2,表示左边减少一个像素，右边同样减少1个像素。

**inflate和inflate_ip**方法的区别是：

- inflate返回一个新的Rect对象，不会修改调用Rect对象的属性
- inflate_ip不返回新的Rect对象，会修改调用Rect对象的属性

现在，我们就利用inflate方法来实现一下食物在出现时，由小变大的动画效果。

首先，在食物类的random_rect方法中，设置食物大小的初始矩形区域，代码如下：

```python
def random_rect(self):
    col=SCREEN_RECT.W/CELL_SIZE-1#屏幕上小格子的列数
    row=SCREEN_RECT.h/CELL_SIZE-1#屏幕上小格子的行数
    x=random.randint(e,col)*CELL_SIZE
    y=random.randint(e,row)*CELL_SIZE
    self.rect-pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
    #食物初始不可见
    self.rect.inflate_ip(-CELL_SIZE,-CELL_SIZE)
```

然后，修改**draw**方法，在绘制食物前，判断一下食物的矩形区域宽度，如果还没有和小格子宽度一致，则向四周放大，代码如下：

```PYTHON
def draw ( self , window ) :
    #判断宽度是否达到小格子宽度
    if self.rect.W<CELL_SIZE:
        self.rect.inflate_ip(2,2)#向四周各自放大1个像素
    pygame.draw.ellipse(window,self.color,self.rect)
```

##### 4.8.4 阶段性小结

- draw模块提供了一系列方法，可以方便地绘制图形：
  - ect绘制矩形
  -  ellipse绘制楠圆
- 定义SCREEN_RECT和CELL_SIZE常量可以方便计算食物的出现位置
- inflate和inflate_ip方法可以方便地缩放矩形，参数务必要是偶数
- 在游戏循环中，每一赖绘制的结果相差不大，在视觉上就会产生一个连续播放的动画效果

####  4.9 定时器时间

按照贪吃蛇的游戏规则描述，如果食物出现的30秒内，贪吃蛇没有吃到食物，那么：

- 被吃到的食物从屏幕上消失
- 在游戏窗口的其他任一随机位置再次出现新的食物

现在如果暂时不考虑贪吃蛇吃食物的情况，要实现游戏规则的需求，我们只需要每隔30秒让食物对象调用一下random_rect方法即可。

这种每隔一段时间，重复执行一个固定动作的场景，我们可以使用定时器事件来实现。pygame的time模块中提供的set_timer方法，就是专门用来定义定时器事件的。

要定义定时器事件，一共需要3个步骤：

1. 义定时器事件代号常量
2. 用set_timer方法设置定时器事件
3. 游戏循环中监听定时器事件



##### 4.9.1设置定时器事件

首先，在game_item.py模块中定义定时器事件常量，代码如下：

```python
FOOD_UPDATE_EVENT =pygame.USEREVENT
```

提示：

- 事件代号是一个整数，初始值可以使用pygame.USEREVENT
- 如果要定义多个事件代号，可以从pygame.USEREVENT开始顺序递增。然后，在Food类random_rect的末尾，设置定时器事件，代码如下：