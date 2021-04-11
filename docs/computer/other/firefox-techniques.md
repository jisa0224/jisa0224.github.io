# Firefox 使用技巧

## 顯示完整網址

預設會隱藏 `http`。

在網址列輸入 `about:config` 按 Enter，搜尋 `browser.urlbar.trimURLs` 設為 `false`。

參考資料: [How to show the full URL in Firefox - CNET](https://www.cnet.com/how-to/how-to-show-the-full-url-in-firefox/)

## 使用滑鼠滾輪切換分頁

在網址列輸入 `about:config` 按 Enter，搜尋 `toolkit.tabbox.switchByScrolling` 設為 `true`。

參考資料: [Is there way switch tabs using mouse wheel? | Firefox Support Forum | Mozilla Support](https://support.mozilla.org/en-US/questions/1285434)

## 關閉 Pocket 功能

在網址列輸入 `about:config` 按 Enter，搜尋 `extensions.pocket.enabled` 設為 `false`。

參考資料: [Disable or re-enable Pocket for Firefox | Firefox Help](https://support.mozilla.org/en-US/kb/disable-or-re-enable-pocket-for-firefox)

## 避免產生大量 datareporting

預設會在 `~/.mozilla/firefox/*.default-release/datareporting/archived/*/` 中產生大量的檔案。

在網址列輸入 `about:config` 按 Enter，搜尋 `toolkit.telemetry.archive.enabled` 設為 `false`，然後刪除 `~/.mozilla/firefox/*.default-release/datareporting/archived`。

參考資料: [1242672 - Provide a way to reduce the size of folder(ProfD\datareporting\archived)](https://bugzilla.mozilla.org/show_bug.cgi?id=1242672)

## 關閉 telemetry

在網址列輸入 `about:config` 按 Enter，分別搜尋 `telemetry` 和 `datareporting` 並設定

```
# Firefox 87.0 Linux
app.update.lastUpdateTime.telemetry_modules_ping    刪除
browser.newtabpage.activity-stream.feeds.telemetry    false
browser.newtabpage.activity-stream.telemetry    false
browser.ping-centre.telemetry    false
browser.urlbar.eventTelemetry.enabled    false
dom.security.unexpected_system_load_telemetry_enabled    false
identity.fxaccounts.account.telemetry.sanitized_uid    刪除
network.trr.confirmation_telemetry_enabled    false
privacy.trackingprotection.origin_telemetry.enabled    false
security.app_menu.recordEventTelemetry    false
security.certerrors.recordEventTelemetry    false
security.identitypopup.recordEventTelemetry    false
security.protectionspopup.recordEventTelemetry    false
services.settings.main.search-telemetry.last_check    刪除
toolkit.telemetry.archive.enabled    false    
toolkit.telemetry.bhrPing.enabled    false
toolkit.telemetry.cachedClientID    刪除
toolkit.telemetry.ecosystemtelemetry.enabled    false
toolkit.telemetry.enabled    false
toolkit.telemetry.firstShutdownPing.enabled    false
toolkit.telemetry.newProfilePing.enabled    false
toolkit.telemetry.shutdownPingSender.enabled    false
toolkit.telemetry.updatePing.enabled    false
datareporting.healthreport.uploadEnabled    false
```

參考資料: [How to See (and Disable) the Telemetry Data Firefox Collects About You](https://www.howtogeek.com/557929/how-to-see-and-disable-the-telemetry-data-firefox-collects-about-you/)