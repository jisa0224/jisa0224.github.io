# X Window System: X Client 如何與 X Server 通訊

X Window System Protocol 只定義了 X Client 與 X Server 間的通訊協定，卻沒有規範如何實做，即具體使用哪種 IPC (Inter-Process Communication) 技術。

本文透過追蹤 [XCB (X protocol C-language Binding)](https://xcb.freedesktop.org/) 函式庫的實做，來了解 X Client 和 X Server 間如何通訊。

開發環境為 Linux，XCB 版本為 [libxcb 1.14](https://lists.x.org/archives/xorg-announce/2020-February/003039.html)。

本文會以 [XCB - Wikipedia](https://en.wikipedia.org/wiki/XCB) 中所提供的範例來追蹤函式。

## 建立連線

來看連線相關的程式碼 (以下省略其它部份的內容)。

``` c
#include <xcb/xcb.h>

int main(void)
{
  xcb_connection_t    *c;

  // open connection to the server
  c = xcb_connect(NULL,NULL);
  if (xcb_connection_has_error(c)) {
    printf("Cannot open display\n");
    exit(EXIT_FAILURE);
  }
  
  // 這裡是主要程式功能

  // close connection to server
  xcb_disconnect(c);

  exit(EXIT_SUCCESS);
}
```

追蹤 `xcb_connect()`

``` c
// src/xcb.h

/**
 * @brief Connects to the X server.
 * @param displayname The name of the display.
 * @param screenp A pointer to a preferred screen number.
 * @return A newly allocated xcb_connection_t structure.
 *
 * Connects to the X server specified by @p displayname. If @p
 * displayname is @c NULL, uses the value of the DISPLAY environment
 * variable. If a particular screen on that server is preferred, the
 * int pointed to by @p screenp (if not @c NULL) will be set to that
 * screen; otherwise the screen will be set to 0.
 *
 * Always returns a non-NULL pointer to a xcb_connection_t, even on failure.
 * Callers need to use xcb_connection_has_error() to check for failure.
 * When finished, use xcb_disconnect() to close the connection and free
 * the structure.
 */
xcb_connection_t *xcb_connect(const char *displayname, int *screenp);

// src/xcb_util.c

xcb_connection_t *xcb_connect(const char *displayname, int *screenp)
{
    return xcb_connect_to_display_with_auth_info(displayname, NULL, screenp);
}
```

在我的電腦上，環境變數 `DISPLAY` 的值是 `:0`，所以範例程式中的 `xcb_connect(NULL,NULL)` 展開來會變成 `xcb_connect(displayname = ":0", screenp = NULL)`。

根據[X11R7.7 的 man pages](https://www.x.org/releases/X11R7.7/doc/man/man7/X.7.xhtml)，每個 X Server 都會有一個 Display name，
格式為 `[hostname]:displaynumber.[screennumber]`。

`:0` 相當於 `localhost:0.0`。

追蹤 `xcb_connect_to_display_with_auto_info()`

``` c
// src/xcb.h

/**
 * @brief Connects to the X server, using an authorization information.
 * @param display The name of the display.
 * @param auth The authorization information.
 * @param screen A pointer to a preferred screen number.
 * @return A newly allocated xcb_connection_t structure.
 *
 * Connects to the X server specified by @p displayname, using the
 * authorization @p auth. If a particular screen on that server is
 * preferred, the int pointed to by @p screenp (if not @c NULL) will
 * be set to that screen; otherwise @p screenp will be set to 0.
 *
 * Always returns a non-NULL pointer to a xcb_connection_t, even on failure.
 * Callers need to use xcb_connection_has_error() to check for failure.
 * When finished, use xcb_disconnect() to close the connection and free
 * the structure.
 */
xcb_connection_t *xcb_connect_to_display_with_auth_info(const char *display, xcb_auth_info_t *auth, int *screen);

// src/xcb_util.c

xcb_connection_t *xcb_connect_to_display_with_auth_info(const char *displayname, xcb_auth_info_t *auth, int *screenp)
{
    int fd, display = 0;
    char *host = NULL;
    char *protocol = NULL;
    xcb_auth_info_t ourauth;
    xcb_connection_t *c;

    int parsed = _xcb_parse_display(displayname, &host, &protocol, &display, screenp);

    if(!parsed) {
        c = _xcb_conn_ret_error(XCB_CONN_CLOSED_PARSE_ERR);
        goto out;
    }

    fd = _xcb_open(host, protocol, display);

    if(fd == -1) {
        c = _xcb_conn_ret_error(XCB_CONN_ERROR);
        goto out;
    }

    if(auth) {
        c = xcb_connect_to_fd(fd, auth);
        goto out;
    }

    if(_xcb_get_auth_info(fd, &ourauth, display))
    {
        c = xcb_connect_to_fd(fd, &ourauth);
        free(ourauth.name);
        free(ourauth.data);
    }
    else
        c = xcb_connect_to_fd(fd, 0);

    if(c->has_error)
        goto out;

    /* Make sure requested screen number is in bounds for this server */
    if((screenp != NULL) && (*screenp >= (int) c->setup->roots_len)) {
        xcb_disconnect(c);
        c = _xcb_conn_ret_error(XCB_CONN_CLOSED_INVALID_SCREEN);
        goto out;
    }

out:
    free(host);
    free(protocol);
    return c;
}
```

追蹤 `_xcb_parse_display()`

``` c
// src/xcb_util.c

static int _xcb_parse_display(const char *name, char **host, char **protocol,
                      int *displayp, int *screenp)
{
    int len, display, screen;
    char *slash, *colon, *dot, *end;

    if(!name || !*name)
        name = getenv("DISPLAY");
    if(!name)
        return 0;

    slash = strrchr(name, '/');

    if (slash) {
        len = slash - name;
        if (protocol) {
            *protocol = malloc(len + 1);
            if(!*protocol)
                return 0;
            memcpy(*protocol, name, len);
            (*protocol)[len] = '\0';
        }
        name = slash + 1;
    } else
        if (protocol)
            *protocol = NULL;

    colon = strrchr(name, ':');
    if(!colon)
        goto error_out;
    len = colon - name;
    ++colon;
    display = strtoul(colon, &dot, 10);
    if(dot == colon)
        goto error_out;
    if(*dot == '\0')
        screen = 0;
    else
    {
        if(*dot != '.')
            goto error_out;
        ++dot;
        screen = strtoul(dot, &end, 10);
        if(end == dot || *end != '\0')
            goto error_out;
    }
    /* At this point, the display string is fully parsed and valid, but
     * the caller's memory is untouched. */

    *host = malloc(len + 1);
    if(!*host)
        goto error_out;
    memcpy(*host, name, len);
    (*host)[len] = '\0';
    *displayp = display;
    if(screenp)
        *screenp = screen;
    return 1;

error_out:
    if (protocol) {
        free(*protocol);
        *protocol = NULL;
    }

    return 0;
}
```

在 `_xcb_parse_display()` 函數裡，代表 Display name 的 `name` 會被拆解成 `protocol`, `host`, `displayp`, `screenp` 四部份分別放入變數中。

追蹤 `_xcb_open()`

``` c
// src/xcb_util.c

static int _xcb_open(const char *host, char *protocol, const int display)
{
    int fd;
    static const char unix_base[] = "/tmp/.X11-unix/X";
    const char *base = unix_base;
    size_t filelen;
    char *file = NULL;
    int actual_filelen;

    /* If protocol or host is "unix", fall through to Unix socket code below */
    if ((!protocol || (strcmp("unix",protocol) != 0)) &&
        (*host != '\0') && (strcmp("unix",host) != 0))
    {
        /* display specifies TCP */
        unsigned short port = X_TCP_PORT + display;
        return _xcb_open_tcp(host, protocol, port);
    }

    {
        filelen = strlen(base) + 1 + sizeof(display) * 3 + 1;
        file = malloc(filelen);
        if(file == NULL)
            return -1;

        /* display specifies Unix socket */
        actual_filelen = snprintf(file, filelen, "%s%d", base, display);    // actual_filelen 被設為 "/tmp/.X11-unix/X0"
    }

    if(actual_filelen < 0)
    {
        free(file);
        return -1;
    }
    /* snprintf may truncate the file */
    filelen = MIN(actual_filelen, filelen - 1);
    fd = _xcb_open_unix(protocol, file);
    free(file);

    if (fd < 0 && !protocol && *host == '\0') {
            unsigned short port = X_TCP_PORT + display;
            fd = _xcb_open_tcp(host, protocol, port);
    }

    return fd;
    return -1; /* if control reaches here then something has gone wrong */
}
```

追蹤 `_xcb_open_unix()`

``` c
// src/xcb_util.c

static int _xcb_open_unix(char *protocol, const char *file)
{
    int fd;
    struct sockaddr_un addr;
    socklen_t len = sizeof(int);
    int val;

    if (protocol && strcmp("unix",protocol))
        return -1;

    strcpy(addr.sun_path, file);
    addr.sun_family = AF_UNIX;
    fd = _xcb_socket(AF_UNIX, SOCK_STREAM, 0);
    if(fd == -1)
        return -1;
    if(getsockopt(fd, SOL_SOCKET, SO_SNDBUF, &val, &len) == 0 && val < 64 * 1024)
    {
        val = 64 * 1024;
        setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &val, sizeof(int));
    }
    if(connect(fd, (struct sockaddr *) &addr, sizeof(addr)) == -1) {
        close(fd);
        return -1;
    }
    return fd;
}
```

追蹤 `_xcb_socket()`

``` c
// src/xcb_util.c

static int _xcb_socket(int family, int type, int proto)
{
    int fd;

    {
        fd = socket(family, type, proto);
        if (fd >= 0)
            fcntl(fd, F_SETFD, FD_CLOEXEC);
    }
    return fd;
}
```

## 總結

以下是函式呼叫鏈

```
xcb_connect(NULL, NULL)
    xcb_connect_to_display_with_auth_info(displayname, NULL, screenp)
        _xcb_parse_display(displayname, &host, &protocol, &display, screenp)
        _xcb_open(host, protocol, display)
            _xcb_open_unix(protocol, file)
                _xcb_socket(AF_UNIX, SOCK_STREAM, 0)
                    socket(family, type, proto)
                connect(fd, (struct sockaddr *) &addr, sizeof(addr))
```

`xcb_connect()` 所作的兩大工作，就是先找出 X Server 的 Display name 並分解為 protocol, hostname, display number, screen number 四個部份，
接著透過 [Berkeley socket API](https://en.wikipedia.org/wiki/Berkeley_sockets) 的方式連接到 X Server，`:0` 在本機上就是 `/tmp/.X11-unix/X0` 這個 socket 檔案。

## 結論

在本機上 X Client 透過 Berkeley socket API 連接到 `/tmp/.X11-unix/X0` 與 X Server 通訊。