# Android 登入 Gmail 但不要加入 Google 帳號到手機

在 Android 手機登入任何一個 Google 服務後，手機會自動把 Google 帳號加入到手機裡，之後所有有使用 Google API 的 App 都會被登入（或者詢問要不要使用這個帳號登入）。

但如果只想登入 Gmail 但不想加入 Google 帳號到手機，目前只能使用 IMAP 的方式，方法如下：

在 Gmail "新增其它帳戶" 的地方選 "其他"，然後選擇 "個人 (IMAP)"，填好 Gmail 帳號密碼後，填寫下列資料：

```
Incoming server name: imap.gmail.com
Port: 993
Encryption: SSL
Outgoing server name: smtp.gmail.com
Port: 465
Encryption: SSL
```

以上資料是參考資料裡寫的，但我使用時它只要求我填內送伺服器和外送伺服器。

Google Workspace (原稱為 G Suite) 的帳號，也是使用這組伺服器。

參考資料：[How to add Gmail account without adding Google account on Android - Gmail Community](https://support.google.com/mail/thread/16222360?hl=en)