## About This Game

This game is inspired by **Doodle Jump**, and some of the images used in this project are taken from the internet. All copyright and ownership of the original game elements, such as graphics, character design, and gameplay mechanics, belong to their respective creators and designers.

The code and content showcased here are purely for **learning** and **educational purposes**. They are intended to demonstrate programming skills and explore game development concepts. The project is not for profit, and I do not claim ownership of the original elements.

I respect the intellectual property rights of the creators, and this work should not be used for any commercial purpose.



## Rules

Most of the rules of this simulated game follows those of the original mobile game, including the types of platforms, the props and the mechanism. 

### Platforms

- Green platforms: also the normal platforms. 
- Blue platforms: (horizontal) moving platforms. 
- Yellow platforms: (vertical) shifting platforms. 

- Brown platforms: the broken platforms, which break. 

- White platforms: the disappearing platforms. 


### Machanisms

#### Blue Platform moving machanism

- 蓝色平台水平移动。从被创造那一刻开始，沿着水平方向左右移动，边界为两端/中线

```python
# pseudoCode
if state == static:
  move_left = False
  move_right = False
  if rect.left == 0 or rect.left == screen_width/2:
    move_right = True
  elif rect.right == screen_width/2 or rect.right == screen_width:
    move_left = True
  state = moving
  
elif state == moving:
  if move_left:
    rect.centerx -= speed
  elif move_right:
    rect.centerx += speed
  
  if rect.left <= 0:
    rect.left = 0
    state = static
  elif rect.right >= screen_width:
    rect.right = screen_width
    state = static
  elif rect.left < screen_width/2 and rect.right >= screen_width/2:
    rect.right = screen_width/2
  elif rect.left > screen_width/2:
    
```

#### Yellow platform moving machanism

- 黄色平台垂直移动，从被创造那一刻开始，沿着垂直方向移动，边界为起点上下某一固定值

```python
11
```

