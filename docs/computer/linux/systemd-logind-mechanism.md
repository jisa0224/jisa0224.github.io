# systemd-logind 原理

kernel 啟動 /sbin/init (指向 /lib/systemd/systemd) 後
systemd 啟動 default.target (指向 graphics.target)
graphics.target REQUIRES multi-user.target
multi-user.target REQUIRES systemd-logind.service
systemd-logind.service ExecStart /usr/lib/systemd/systemd-logind

For TTYS:
    systemd-logind 會啟動 /sbin/agetty (ref: man systemd-logind.service)
    /sbin/agetty 啟動 /sbin/login
    /sbin/login 使用 PAM 模組 /etc/pam.d/login
    /etc/pam.d/login INCLUDE /etc/pam.d/system-local-login，後者又 INCLUDE /etc/pam.d/system-login
    /etc/pam.d/system-login 在 session 使用 pam_systemd.so

For Graphical:
    graphics.target Wants display-manager.service (/etc/systemd/system/display-manager.service -> /usr/lib/systemd/system/sddm.service)
    sddm.service 執行 /usr/bin/sddm
    /usr/bin/sddm 使用 PAM 模組 /etc/pam.d/sddm
    /etc/pam.d/sddm INCLUDE /etc/pam.d/system-login
    /etc/pam.d/system-login 在 session 使用 pam_systemd.so

pam_systemd.so 向 systemd-logind.service 註冊 session (建立 session scope, per-user slice 等) (ref: man pam_systemd)


* /usr/bin/sddm 執行 /usr/bin/sddm-greeter，不確定哪個才是真正負責驗證登入(使用 PAM 模組)的