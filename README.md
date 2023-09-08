# Simple Paint Programming Language
<img src="pic.png" alt="Image Description" width="200"/>
### Overview
We were tasked with creating a Python interpreter for a programming language known as SPPL (Simple Paint Programming Language). 
SPPL enables users to write code that generates images based on their instructions. The interpreter is hosted on a server, and clients connect to it, 
sending their code in JSON format.

The server processes the code and returns either an image or an error message (in cases of syntax or runtime errors) for the client to download.

### Language rules:

In SPPL code, the first line specifies the image's dimensions (length and width) as two integers separated by a space.

Expressions in SPPL can include positive numbers or zero, along with addition, subtraction, multiplication, division, or remainder operations.

Every SPPL program must contain a function called "main" with no arguments. Programs lacking this function are considered invalid.

prebuilt SPPL functions are:

| Function Call | Return Value | Description |
|--|--|--|
| if(cond, t, f) | t if cond!=0 else f | conditional expression |
| drawPoint(x, y, r, g, b) | 0 | draw a point on (x,y) cordinate |
| drawLine(x0, y0, x1, y1, r, g, b) | 0 | draw line between two point |
| drawCircle(x, y, radius, r, g, b) | 0 | draw circle with center (x,y) |

The r, g, and b arguments represent colors and must be values between 0 and 255.

### Function definition rules:
To define a simple function:

>func functionName(arg1 arg2, ...) expr

This function takes arguments and returns an expression (expr).

To define recursive function:

>rfunc functionName(arg1, arg2, ... , rArg)
>
>0 baseExpr
>
>rVal rExpr

In a recursive function, baseExpr is evaluated first. Initially, rArg is set to zero, and baseExpr does not have access to rArg. The result of baseExpr is stored in rVal. Then, rArg is incremented by 1, and rExpr is evaluated, which can include both rVal and the current rArg. The result of rExpr is once again stored in rVal, and rExpr is called with rArg+1. This process continues until rArg reaches the specified input rArg, at which point the recursion terminates. This recursive approach helps implement loops in SPPL.

### Converting SPPL Program Strings to JSON
The server only accepts JSON-formatted code, so clients must be able to convert their program code to JSON format. 

### Examples
For examples of both valid and invalid SPPL programs, along with the JSON representation of a valid program, please refer to the samples.
