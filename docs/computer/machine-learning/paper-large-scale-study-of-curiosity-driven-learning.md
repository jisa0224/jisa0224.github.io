# [讀論文] Large-Scale Study of Curiosity-Driven Learning

名稱：Large-Scale Study of Curiosity-Driven Learning  
作者：Yuri Burda, Harri Edwards, Deepak Pathak, Amos Storkey, Trevor Darrell, Alexei A. Efros  
發表時間：2018/8/13  
論文檔案、說明、程式碼：[Large-Scale Study of Curiosity-Driven Learning](https://pathak22.github.io/large-scale-curiosity/)  
其它：[This Curious AI Beats Many Games...and Gets Addicted to the TV - YouTube](https://www.youtube.com/watch?v=fzuYEStsQxc)

## 摘要

Reinforcement learning algorithms rely on carefully engineering environment rewards that are extrinsic to the agent. However, annotating each environment with hand-designed, dense rewards is not scalable, motivating the need for developing reward functions that are intrinsic to the agent. Curiosity is a type of intrinsic reward function which uses prediction error as reward signal.

In this paper:  
(a) We perform the first large-scale study of purely curiosity-driven learning, i.e. without any extrinsic rewards, across 54 standard benchmark environments, including the Atari game suite. Our results show surprisingly good performance, and a high degree of alignment between the intrinsic curiosity objective and the hand-designed extrinsic rewards of many game environments.  
(b) We investigate the effect of using different feature spaces for computing prediction error and show that random features are sufficient for many popular RL game benchmarks, but learned features appear to generalize better (e.g. to novel game levels in Super Mario Bros.).  
(c) We demonstrate limitations of the prediction-based rewards in stochastic setups.

## 筆記

以往在做 Reinforcement Learning (RL) 的人，都會為他們的演算法設計一個外顯(extrinsic)的目標函數，比如說馬力歐兄弟就是得高分和不死，但這樣的作法會使得他們的演算法只限定於該遊戲，所以本篇作者們就想能不能不要有外顯目標，而是內隱(intrinsic)的目標，換言之，讓程式自己去尋找玩遊戲的意義。

不過目前還沒有不用目標函數的 RL，所以他們把想法放在「預測」上面，他們把目標函數設計成最大化「預測錯誤」，對於一個狀態 $x_t$，agent 做了一個動作 $a_t$，然後轉移到下一個狀態 $a_{t+1}$，而他們的目標函數就是：

給定一個狀態轉移 $\{x_t,x_{t+1},a_t\}$ ，最大化 $r_t=-\log p(\phi (x_{t+1})|x_t,a_t)$

也就是當預測錯誤的情況越多，獎勵就越大，意思就是偏好「沒看過得東西」和「複雜的東西」，因為它們都超出 agent 的預測。

不過我個人很懷疑這樣算不算是內隱的目標，確實他們沒有把分數當成目標，但還是有設定目標。後來我發現我搞錯了，他們的論文不是「不要有目標」而是「不要有外顯的目標」，內顯目標當然可以有，而如果進一步解讀這個目標函數，把它當成「盡量找尋沒看過得東西和沒做過得事」的話，確實是符合他們所謂的「好奇」的預測函數，如果一直做一樣的事或看一樣的東西的話，就會無聊嘛，所以就是「不想無聊」。

這篇論文的一個重點在於怎樣不要讓一個遊戲有外顯的目標，比如分數，以馬力歐兄弟為例，原本的遊戲換關或死亡的時候畫面變化會很明顯，他們把它改成死掉之後重新開始，然後把換關的部份弄的平滑一點，換言之，讓整個遊戲看起來像一個無限大的單一關卡，這樣就不會有過關的閃耀畫面（這會被當成外顯目標）。

這篇論文的另一個重點放在特徵編碼上，也就是目標函數裡的 $\phi ()$，不過我對這部份比較沒興趣，所以就沒多看。

最後他們探討的是他們提出的「基於預測的獎勵」的限制，前面有提到 agent 會偏好沒看過的東西，所以他們就在遊戲（這邊用的遊戲是在一個3D的虛擬空間裡移動）裡放了一個電視（不斷變化的畫面），然後 agent 就停在那不移動了，因為電視上的內容無法預測，不過似乎最後還是有收斂的樣子。在這邊也有提到熵，不過看不懂就沒看了。
 
