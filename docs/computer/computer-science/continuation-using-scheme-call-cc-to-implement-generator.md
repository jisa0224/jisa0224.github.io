# Continuation: 使用 Scheme 的 call/cc 實現 generator

`call/cc` 即 "call with current continuation"。

## Scheme 的 call/cc

``` scheme
(define global-continuation #f)
(define generator-continuation #f)

(define generator
  (lambda (n)
    (call/cc (lambda (c)
               (set! generator-continuation c)
               (global-continuation n)))        ; 等價於 Python 的 yield
    (generator (+ n 1))))                       ; 因為沒有 while 可用，使用尾遞迴的方式取代

(define init-generator
  (lambda ()
    (call/cc (lambda (c)
               (set! global-continuation c)
               (generator 0)))))

(define next
  (lambda ()
    (call/cc (lambda (c)
               (set! global-continuation c)
               (generator-continuation #f)))))

(init-generator)

(display (next))(newline)
(display (next))(newline)
(display (next))(newline)
(display (next))(newline)
(display (next))(newline)
```

輸出:

```
1
2
3
4
5
```

## 等價的 Python 程式碼

``` python
def Generator():
    n = 0
    while True:
        n += 1
        yield n

generator = Generator()

print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
```

輸出和上面一樣。