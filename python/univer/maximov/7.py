
import turtle

def getStep(axiom, newF, newB, step_num):

    res = axiom
    for each in range(step_num - 1):
        res = res.replace("b", newB).replace("F", newF)

    return res

axiom = "F+F+F+F"
newF = "F+b-F-FFF+F+B-F"
newB = "bbb"

step_len = 10
size = 2000
i = 5
t = turtle.Turtle()
t.speed(10000000)
t.screen.delay(0)
t.screen.setworldcoordinates(-size,-size,size,size)
t.penup()
t.setx(-size/2)
t.sety(size/2)
t.begin_fill()
t.pendown()
t.resizemode("auto")
# TurtleScreen.setworldcoordinates(0, 0,1000,1000)

# for i in range(1, 5):
current_ste = 0
for repeat in range(1):
    step = getStep(axiom, newF, newB, i)
    whole_step_count = len(step.replace('+', '').replace('-',''))
    print("\n\n\n\n\n-------------------------------------")
    print("Step number: " + str(i))
    print("Step: " + step)

    for each in step:
        print(f"whole steps: {str(whole_step_count)} current step: " + str(current_ste))
        
        current_ste = current_ste + 1
        if each == "+":
            t.left(90)
        elif each == "-":
            t.right(90)
        else:
            if each == "F":
                t.forward(step_len)
            else: 
                t.penup()
                t.forward(step_len)
                t.pendown()


t.screen.exitonclick()
t.screen.mainloop()