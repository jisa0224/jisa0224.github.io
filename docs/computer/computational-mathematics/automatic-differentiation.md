# 自動微分 Automatic Differentiation(未完成)

## 範例

給定一個二元函數

$$ z(x,y) = x^2 + 2y + \sin{xy} $$

求 

$$ \begin{aligned}
z(2,3) & \\
\\
\frac{\partial z}{\partial x}(2,3) & \\
\\
\frac{\partial z}{\partial y}(2,3) &
\end{aligned} $$

### 符號微分

符號微分可得

$$ \begin{aligned}
& \frac{\partial z}{\partial x} = 2x + y \cos{xy} \\
& \frac{\partial z}{\partial y} = 2 + x \cos{xy}
\end{aligned} $$

代入 $(x,y) = (2,3)$

$$ \begin{aligned}
z(2,3) & = 10 + \sin 6 \\
\\
\frac{\partial z}{\partial x}(2,3) & = 4 + 3 \cos 6 \\
\\
\frac{\partial z}{\partial y}(2,3) & = 2 + 2 \cos 6
\end{aligned} $$

### 自動微分

先分解 $z(x,y)$

``` mermaid
graph LR
    x(("x")) -- "v₁ = x" --> v1(("v₁"))
    y(("y")) -- "v₂ = y" --> v2(("v₂"))

    v1 -- "v₃ = v₁²" --> v3(("v₃"))
    v1 & v2 -- "v₅ = v₁ v₂" --> v5(("v₅"))
    v2 -- "v₄ = 2 v₂" --> v4(("v₄"))

    v5 -- "v₆ = sin v₅" --> v6(("v₆"))

    v3 & v4 & v6 -- "v₇ = v₃ + v₄ + v₆" --> v7(("v₇"))

    v7 -- "z = v₇" --> z(("z"))
```

$$ \begin{aligned}
& x \\
& y \\
\\
& v_1 = x \\
& v_2 = y \\
\\
& v_3 = {v_1}^2 \\
& v_4 = 2v_2 \\
\\
& v_5 = v_1 v_2 \\
& v_6 = \sin v_5 \\
\\
& v_7 = v_3 + v_4 + v_6 \\
\\
& z = v_7
\end{aligned} $$

#### 前向模式 Forward Mode

<table width="100%">
<tr><th>Forward Evaluation Trace</th><th>Forward Derivative Trace</th></tr>
<tr><td width="50%">
$$ \begin{aligned}
& x = 2 \\
& y = 3 \\
\\
& v_1 = x = 2 \\
& v_2 = y = 3 \\
\\
& v_3 = {v_1}^2 = 4 \\
& v_4 = 2v_2 = 6 \\
\\
& v_5 = v_1 v_2 = 6 \\
& v_6 = \sin v_5 = \sin 6 \\
\\
& v_7 = v_3 + v_4 + v_6 = 10 + \sin 6 \\
\\
& z = v_7 = 10 + \sin 6
\end{aligned} $$
</td><td width="50%">
$$ \begin{aligned}
& \frac{\partial x}{\partial x} = 1 \\
& \frac{\partial y}{\partial x} = 0\\
\\
& \frac{\partial v_1}{\partial x} = \frac{\partial x}{\partial x} = 1 \\
& \frac{\partial v_2}{\partial x} = \frac{\partial y}{\partial x} = 0\\
\\
& \frac{\partial v_3}{\partial x} = 2v_1 \frac{\partial v_1}{\partial x} = 4 \\
& \frac{\partial v_4}{\partial x} = 2 \frac{\partial v_2}{\partial x} = 0 \\
\\
& \frac{\partial v_5}{\partial x} = \frac{\partial v_1}{\partial x} v_2 + v_1 \frac{\partial v_2}{\partial x}= 3 \\
& \frac{\partial v_6}{\partial x} = \cos v_5 \times \frac{\partial v_5}{\partial x}= 3 \cos 6 \\
\\
& \frac{\partial v_7}{\partial x} = \frac{\partial v_3}{\partial x} + \frac{\partial v_4}{\partial x} + \frac{\partial v_6}{\partial x} = 4 + 3 \cos 6 \\
\\
& \frac{\partial z}{\partial x} = \frac{\partial v_7}{\partial x} = 4 + 3 \cos 6
\end{aligned} $$
</td></tr></table>

求 $\frac{\partial z}{\partial y}$ 同理，這裡省略。

#### 反向模式 Reverse Mode

<table width="100%">
<tr><th>Forward Evaluation Trace</th><th>Reverse Adjoint Trace</th></tr>
<tr><td width="50%">
$$ \begin{aligned}
& x = 2 \\
& y = 3 \\
\\
& v_1 = x = 2 \\
& v_2 = y = 3 \\
\\
& v_3 = {v_1}^2 = 4 \\
& v_4 = 2v_2 = 6 \\
\\
& v_5 = v_1 v_2 = 6 \\
& v_6 = \sin v_5 = \sin 6 \\
\\
& v_7 = v_3 + v_4 + v_6 = 10 + \sin 6 \\
\\
& z = v_7 = 10 + \sin 6
\end{aligned} $$
</td><td width="50%">
$$ \begin{aligned}
& \frac{\partial z}{\partial z} = 1 \\
\\
& \frac{\partial z}{\partial v_7} = \frac{\partial z}{\partial z} = 1 \\
\\
& \frac{\partial z}{\partial v_3} = \frac{\partial z}{\partial v_7} \frac{\partial v_7}{\partial v_3} = 1 \times 1 = 1 \\
& \frac{\partial z}{\partial v_4} = \frac{\partial z}{\partial v_7} \frac{\partial v_7}{\partial v_4} = 1 \times 1 = 1 \\
& \frac{\partial z}{\partial v_6} = \frac{\partial z}{\partial v_7} \frac{\partial v_7}{\partial v_6} = 1 \times 1 = 1 \\
& \frac{\partial z}{\partial v_5} = \frac{\partial z}{\partial v_6} \frac{\partial v_6}{\partial v_5} = 1 \times \cos v_5 = \cos 6 \\
\\
& \frac{\partial z}{\partial v_1} = \frac{\partial z}{\partial v_3} \frac{\partial v_3}{\partial v_1} + \frac{\partial z}{\partial v_5} \frac{\partial v_5}{\partial v_1} = 1 \times 2v_1 + \cos 6 \times v_2 = 4 + 3 \cos 6 \\
& \frac{\partial z}{\partial v_2} = \frac{\partial z}{\partial v_4} \frac{\partial v_4}{\partial v_2} + \frac{\partial z}{\partial v_5} \frac{\partial v_5}{\partial v_2} = 1 \times 2 + \cos 6 \times v_1 = 2 + 2 \cos 6 \\
\\
& \frac{\partial z}{\partial x} = \frac{\partial z}{\partial v_1} = 4 + 3 \cos 6 \\
& \frac{\partial z}{\partial y} = \frac{\partial z}{\partial v_2} = 2 + 2 \cos 6
\end{aligned} $$
</td></tr></table>

註：右邊的 Reverse Adjoint Trace 是由上往下看，跟參考資料的方向相反。

特別要注意 $\frac{\partial z}{\partial v_1}$ 和 $\frac{\partial z}{\partial v_2}$ 必須要用到 Chain rule 中的「多元複合函數求導法則」

> 考慮函數 $z = f(x, y)$，其中 $x = g(t)$，$y = h(t)$，$g(t)$ 和 $h(t)$ 是可微函數，那麼：
> $$ {\ dz \over dt}={\partial z \over \partial x}{dx \over dt}+{\partial z \over \partial y}{dy \over dt} $$
> [*連鎖法則 - 維基百科，自由的百科全書*](https://zh.wikipedia.org/wiki/%E9%93%BE%E5%BC%8F%E6%B3%95%E5%88%99#%E5%A4%9A%E5%85%83%E5%A4%8D%E5%90%88%E5%87%BD%E6%95%B0%E6%B1%82%E5%AF%BC%E6%B3%95%E5%88%99)

可以從圖中看出 $z$ 到 $v_1$ 的路徑會經過 $v3$ 和 $v5$，相當於上式中的 $x$ 和 $y$，$v_1$ 則是上式中的 $t$。

#### 觀察結果

1. 不論是前向還是反向模式，計算時都只會用到圖上前一個節點以及 Forward Evaluation Trace 的計算結果。
2. 如果輸入節點很多的時候且全部要求出偏導數的時候，用反向模式會比較節省時間，因為一次就可以全部算出來。

## 參考資料

[自动微分(Automatic Differentiation)简介_人工智能_CarlXie-CSDN博客](https://blog.csdn.net/aws3217150/article/details/70214422)  
[附录 D、自动微分 - 反向自动微分 - 《Sklearn 与 TensorFlow 机器学习实用指南》 - 书栈网 · BookStack](https://www.bookstack.cn/read/hands_on_Ml_with_Sklearn_and_TF/spilt.5.docs-D.%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)
