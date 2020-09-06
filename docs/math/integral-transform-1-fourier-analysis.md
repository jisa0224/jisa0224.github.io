# 積分變換(一)：傅立葉分析(未完成)

## 三角函數與週期波

### 三角函數的恆等式

推導過程中會用到一些三角函數的恆等式，整理如下：

- 反射於 $\theta =0$
  $$ \begin{aligned}
  \sin(-\theta) & = -\sin(\theta) \\
  \cos(-\theta) & = \cos(\theta)
  \end{aligned} $$
- 移位 $\frac{\pi}{2}$
  $$ \begin{aligned}
  \sin(\theta+\frac{\pi}{2}) & = \cos \theta \\
  \cos(\theta-\frac{\pi}{2}) & = \sin \theta
  \end{aligned} $$
- 和差公式
  $$ \begin{aligned}
  \sin(\alpha \pm \beta)&=\sin \alpha \cos \beta \pm \cos \alpha \sin \beta \\
  \cos(\alpha \pm \beta)&=\cos \alpha \cos \beta \mp \sin \alpha \sin \beta
  \end{aligned} $$
- 線性組合
  $$ a\cos x + b\sin x = \sqrt{a^2 + b^2} \cos(x - \phi) $$
  其中 $\phi = \tan^{-1} \frac{b}{a}$

根據以上的公式，可以得知正弦波可以表示成

- 振幅-相位形式
  $$ \begin{aligned}
  f(t) & = A \cos(\omega t + \phi) \\
  & = A \sin(\omega t + (\phi - \frac{\pi}{2}))
  \end{aligned} $$

- Sine-Cosine 形式
  $$ f(t) = a \cos(\omega t) + b \sin(\omega t) $$

  其中 $\begin{cases} a = A \cos(\phi) \\ b = -A \sin(\phi) \end{cases}$，推導如下

  $$ \begin{aligned}
  f(t) & = A \cos(\omega t + \phi) \\
  & = A \cos(\omega t)\cos(\phi) - A \sin(\omega t)\sin(\phi) \\
  & = \color{red}{A \cos(\phi)} \cos(\omega t) \color{blue}{- A \sin(\phi)} \sin(\omega t) \\
  & = \color{red}{a} \cos(\omega t) + \color{blue}{b} \sin(\omega t)
  \end{aligned} $$

### 三角函數的指數定義

定義

$$ \begin{cases}
\sin \theta = \frac{e^{i\theta} - e^{-i\theta}}{2i} \\
\cos \theta = \frac{e^{i\theta} + e^{-i\theta}}{2}
\end{cases} $$

因此

$$ e^{i\theta} ＝ \cos \theta + i \sin \theta $$

### 三角函數的正交性

傅立葉變換能夠成立都是基於以下幾個恆等式：

$$ \int_{-\pi}^{\pi} \sin(mx) dx = 0 \\
\int_{-\pi}^{\pi} \cos(mx) dx = 0 $$

$$ \begin{aligned}
& \int_{-\pi}^{\pi} \sin(mx) \sin(nx) dx = \begin{cases}\pi & m = n\\0 & m \neq n\end{cases} \\
& \int_{-\pi}^{\pi} \cos(mx) \cos(nx) dx = \begin{cases}\pi & m = n\\0 & m \neq n\end{cases} \\
& \int_{-\pi}^{\pi} \sin(mx) \cos(nx) dx = 0
\end{aligned} $$

#### 推導

### 週期波的數學表示

表示一個週期波需要波型、振幅 $A$、頻率 $f$（或角頻率 $\omega$ 或週期 $T$）和相位差 $\phi$，如果是正弦波的話可以表示成

$$ f(t) = A \cos(\omega t + \phi) $$

由於 $\sin$ 跟 $\cos$ 只是平移了 $\frac{\pi}{2}$ 個相位差，所以 $\cos$ 也算正弦函數。

## 傅立葉級數

傅立葉級數（FS, Fourier Series）將一個週期函數 $f(t)$ 展開成不同頻率的正弦函數與餘弦函數的線性組合。

### Sine-Cosine 形式

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^\infty a_n \cos(nt) + b_n \sin(nt) $$

其中

$$ a_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt \\
b_n = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \sin(nt) dt $$

### 振幅-相位形式

透過三角恆等式，也可以把 Sine-Cosine 形式換成其它形式

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^\infty A_n \cos(nt + \phi_n) $$
  
其中
  
$$ A_n = \sqrt{a_n^2+b_n^2} \\
  \phi_n = -\tan^{-1} \frac{b_n}{a_n} $$
  
Sine-Cosine 形式中的係數 $a_n$ 和 $b_n$ 沒有物理意義；振幅-相位形式中的係數 $A_n$ 和 $\phi_n$ 則分別代表振幅與相位。

### 指數形式

不過在實際計算上更常用的是指數形式：

$$ f(t) = \sum_{n=-\infty}^{\infty} c_n e^{int} $$

其中

$$ c_n = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) e^{-int} dt $$

且

$$ c_n = \begin{cases}
\frac{a_0}{2} & n = 0 \\
\frac{1}{2} (a_n - i b_n) & n > 0 \\
\frac{1}{2} (a_{|n|} + i b_{|n|}) = c_{|n|}^* & n < 0
\end{cases} $$

$$ A_n = 2 \sqrt{c_n c_{-n}} $$

$c_{|n|}^*$ 表示 $c_{|n|}$ 的共軛複數。

#### 使用指數形式的理由

儘管振幅-相位形式有物理意義，但因為它在 $\sin$ 和 $\cos$ 裡還有一個相位差，導致我們無法使用 [三角函數的正交性](#三角函數的正交性) 中那三個公式來得到係數，所以還是必須回歸到 Sine-Cosine 形式。

但 Sine-Cosine 形式必須分開計算 $a_n$ 和 $b_n$，我們可以使用一個複數來同時表示 $a_n$ 和 $b_n$，在表達上會比較簡潔。

#### 指數形式的推導

從傅立葉級數的 Sine-Cosine 形式開始：

$$ \begin{aligned}
f(t) & = \frac{a_0}{2} + \sum_{n=1}^\infty a_n \cos(nt) + b_n \sin(nt) \\
& = \frac{a_0}{2} + \sum_{n=1}^\infty a_n \frac{e^{int} + e^{-int}}{2} + b_n \frac{e^{int} - e^{-int}}{2i} \\
& = \frac{a_0}{2} + \sum_{n=1}^\infty (\frac{a_n}{2}+\frac{b_n}{2i})e^{int} + (\frac{a_n}{2}-\frac{b_n}{2i})e^{-int} \\
& = \color{red}{\frac{a_0}{2}} + \sum_{n=1}^\infty \color{blue}{\frac{1}{2}(a_n-i b_n)}e^{int} + \color{green}{\frac{1}{2}(a_n+i b_n)}e^{-int} \\
& = \color{red}{c_0} + \sum_{n=1}^\infty \color{blue}{c_n} e^{int} + \color{green}{c_{-n}} e^{i(-n)t} \\
& = \sum_{n=-\infty}^\infty c_n e^{int}
\end{aligned} $$

$$ \begin{aligned}
c_n & = \frac{1}{2} (a_n - i b_n) & n > 0 \\
& = \frac{1}{2} \left( \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt - i \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) (\cos(nt)-i\sin(nt)) dt \\
& = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) (\cos(-nt)+i\sin(-nt)) dt \\
& = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) e^{-int} dt \\
\\
c_n & = \frac{1}{2} (a_{|n|} + i b_{|n|}) & n < 0 \\
& = \frac{1}{2} \left( \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(-nt) dt + i \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \sin(-nt) dt \right) \\
& = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) (\cos(-nt)+i\sin(-nt)) dt \\
& = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) e^{-int} dt
\end{aligned} $$

對於 $n < 0$ 的係數 $c_n$，其計算式與 $n > 0$ 的情況相同

$$ \begin{aligned}
A_n & = \sqrt{a_n^2+b_n^2} \\
& = |2 c_n| \\
& = 2 \sqrt{c_n c_n^*} \\
& = 2 \sqrt{c_n c_{-n}}
\end{aligned} $$

### 週期不是 2π 的情況

仔細看上面 Sine-Cosine 形式的公式

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^\infty a_n \cos(nt) + b_n \sin(nt) $$

會發現我們把 $f(t)$ 分解成角頻率 1, 2, 3, ... ──即 1 的整數倍──的正弦函數與餘弦函數的線性組合。

對於週期為 $T$ 的週期函數 $f(t)$，其傅立葉級數（Sine-Cosine 形式）為

$$ f(t) = \frac{a_0}{2} + \sum_{n=1}^\infty a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) $$

其中

$$ \begin{aligned}
\omega_0 & = \frac{2\pi}{T} \\
a_n & = \frac{2}{T} \int_{t_0}^{t_0+T} f(t) \cos(n\omega_0 t) dt \\
b_n & = \frac{2}{T} \int_{t_0}^{t_0+T} f(t) \sin(n\omega_0 t) dt
\end{aligned} $$

因為只要有積分到一個週期就可以，所以 $t_0$ 可以是任意數，為了積分方便通常都會使用 $t_0 = -\frac{T}{2}$，即

$$ \begin{aligned}
a_n & = \frac{2}{T} \int_{-\frac{T}{2}}^{\frac{T}{2}} f(t) \cos(n\omega_0 t) dt \\
b_n & = \frac{2}{T} \int_{-\frac{T}{2}}^{\frac{T}{2}} f(t) \sin(n\omega_0 t) dt
\end{aligned} $$

把 $f(t)$ 分解成「角頻率 $\omega_0$ 整數倍」的正弦函數與餘弦函數的線性組合。

### 傅立葉正弦級數：偶函數的特殊情況

若 $f(t)$ 為偶函數，則 $f(-t) = f(t)$，其傅立葉級數（Sine-Cosine 形式）退化為

$$ f(t) = \sum_{n=1}^\infty b_n \sin(nt) $$

其中

$$ b_n = \frac{2}{\pi} \int_{0}^{\pi} f(t) \sin(nt) dt $$

推導如下

$$ \begin{aligned}
a_0 & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt \\
& = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) dt \\
& = 0 \\
\\
a_n & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt \\
& = \frac{1}{\pi} \left( \int_{-\pi}^{0} f(t) \cos(nt) dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{-\pi} f(t) \cos(nt) dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(-t)} \color{blue}{\cos(-nt)} dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(t)} \color{blue}{\cos(nt)} dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = 0
\\
b_n & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \sin(nt) dt \\
& = \frac{1}{\pi} \left( \int_{-\pi}^{0} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{-\pi} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(-t)} \color{blue}{\sin(-nt)} dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(t)} \color{blue}{(-\sin(nt))} dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( \int_{0}^{\pi} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{2}{\pi} \int_{0}^{\pi} f(t) \sin(nt) dt
\end{aligned} $$

只剩下 Sine 的項，且相當於只積分半個週期。

即便 $f(t)$ 不是偶函數，還是可以求其傅立葉正弦級數，結果就相當於求 $\begin{cases} f(t) & t \geq 0 \\ f(-t) & t < 0 \end{cases}$ 的傅立葉級數。

### 傅立葉餘弦級數：奇函數的特殊情況

若 $f(t)$ 為奇函數，則 $f(-t) = -f(t)$，其傅立葉級數（Sine-Cosine 形式）退化為

$$ f(t) = a_0 + \sum_{n=1}^\infty a_n \cos(nt) $$

其中

$$ \begin{aligned}
a_0 & = \frac{1}{\pi} \int_{0}^{\pi} f(t) dt \\
a_n & = \frac{2}{\pi} \int_{0}^{\pi} f(t) \cos(nt) dt
\end{aligned} $$

推導如下

$$ \begin{aligned}
a_0 & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt \\
& = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) dt \\
\\
a_n & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \cos(nt) dt \\
& = \frac{1}{\pi} \left( \int_{-\pi}^{0} f(t) \cos(nt) dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{-\pi} f(t) \cos(nt) dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(-t)} \color{blue}{\cos(-nt)} dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{-f(t)} \color{blue}{\cos(nt)} dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{1}{\pi} \left( \int_{0}^{\pi} f(t) \cos(nt) dt + \int_{0}^{\pi} f(t) \cos(nt) dt \right) \\
& = \frac{2}{\pi} \int_{0}^{\pi} f(t) \cos(nt) dt \\
\\
b_n & = \frac{1}{\pi} \int_{-\pi}^{\pi} f(t) \sin(nt) dt \\
& = \frac{1}{\pi} \left( \int_{-\pi}^{0} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{-\pi} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{f(-t)} \color{blue}{\sin(-nt)} dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} \color{red}{(-f(t))} \color{blue}{(-\sin(nt))} dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = \frac{1}{\pi} \left( -\int_{0}^{\pi} f(t) \sin(nt) dt + \int_{0}^{\pi} f(t) \sin(nt) dt \right) \\
& = 0
\end{aligned} $$

只剩下 Cosine 的項，且相當於只積分半個週期。

即便 $f(t)$ 不是奇函數，還是可以求其傅立葉餘弦級數，結果就相當於求 $\begin{cases} f(t) & t \geq 0 \\ f(-t) & t < 0 \end{cases}$ 的傅立葉級數。

### 非週期函數的情況

## 傅立葉級數的線性代數觀點

## 連續傅立葉變換

連續傅立葉變換（CFT, Continuous Fourier Transform）將一個週期函數 $f(t)$ 從時域轉換到頻域。

$$ \hat{f}(\omega) = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) e^{-i\omega t} dt $$

以及其逆轉換：

$$ f(t) = \int_{-\infty}^{\infty} \hat{f}(\omega) e^{i\omega t} d\omega $$

### 推導

觀察傅立葉級數的指數形式：

$$ f(t) = \sum_{n=-\infty}^{\infty} c_n e^{int} $$

其中

$$ c_n = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) e^{-int} dt $$

把 $n$ 換成 $\omega$、$c_n$ 換成 $\hat{f}(\omega)$、$\sum$ 換成 $\int$ 即可。

### 週期不是 2π 的情況

與傅立葉級數相同，對於週期為 $T$ 的週期函數 $f(t)$，其傅立葉轉換為

$$ \hat{f}(\omega) = \frac{1}{T} \int_{t_0}^{t_0+T} f(t) e^{-i\omega t} dt $$

因為只要有積分到一個週期就可以，所以 $t_0$ 可以是任意數，為了積分方便通常都會使用 $t_0 = -\frac{T}{2}$，即
$$ \hat{f}(\omega) = \frac{1}{T} \int_{-\frac{T}{2}}^{\frac{T}{2}} f(t) e^{-i\omega t} dt $$

### 非週期函數的情況

非週期函數其實就是週期無限大的週期函數，所以只要對週期為 $T$ 的傅立葉轉換取極限即可。

$$ \hat{f}(\omega) = \lim_{T \rightarrow \infty} \frac{1}{T} \int_{-\frac{T}{2}}^{\frac{T}{2}} f(t) e^{-i\omega t} dt $$

然而，我並不知道這個極限如何求解，只知道結果應該是

$$ \hat{f}(\omega) = \frac{1}{2\pi} \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt $$

## 離散傅立葉變換

離散傅立葉變換（DFT, Discrete Fourier Transform）

### 快速傅立葉轉換

快速傅立葉轉換（FFT, Fast Fourier Transform）

## 離散時間傅立葉變換

離散時間傅立葉變換（DTFT, Discrete-Time Fourier Transform）

## 參考資料

- 三角函數  
  [三角恆等式 - 維基百科，自由的百科全書](https://zh.wikipedia.org/zh-tw/%E4%B8%89%E8%A7%92%E6%81%92%E7%AD%89%E5%BC%8F)

- 傅立葉分析計算公式  
  [Fourier Analysis—Wolfram Language Documentation](https://reference.wolfram.com/language/guide/FourierAnalysis.html)

- 傅立葉級數  
  [Fourier series - Wikipedia](https://en.wikipedia.org/wiki/Fourier_series)  
  [Fourier Series -- from Wolfram MathWorld](https://mathworld.wolfram.com/FourierSeries.html)  
  [如何理解傅立葉變換中的複數？ | Yahoo奇摩知識+](https://tw.answers.yahoo.com/question/index?qid=20091207000010KK00570)  
  [傅里叶系列（一）傅里叶级数的推导 - 知乎](https://zhuanlan.zhihu.com/p/41455378)

- 傅立葉正弦/餘弦級數  
  [Fourier sine and cosine series - Wikipedia](https://en.wikipedia.org/wiki/Fourier_sine_and_cosine_series)  
  [Half range Fourier series - Wikipedia](https://en.wikipedia.org/wiki/Half_range_Fourier_series)  
  [Fourier Sine Series -- from Wolfram MathWorld](https://mathworld.wolfram.com/FourierSineSeries.html)  
  [Fourier Cosine Series -- from Wolfram MathWorld](https://mathworld.wolfram.com/FourierCosineSeries.html)

- 連續傅立葉變換  
  [傅里叶系列（二）傅里叶变换的推导 - 知乎](https://zhuanlan.zhihu.com/p/41875010)

- 離散傅立葉變換  
  [傅里叶系列（三）离散傅里叶变换（DFT） - 知乎](https://zhuanlan.zhihu.com/p/75521342)
 
