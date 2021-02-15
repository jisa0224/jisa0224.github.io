# C++ Class: default constructor, copy constructor, copy-assignment operator, and destructor

以下程式碼在最前面都包含

```cpp
/* 
 * IMPORTANT: Compile this code with "-fno-elide-constructors" (when using GCC) to turn off constructor optimization!
 * https://en.cppreference.com/w/cpp/language/copy_elision
 */

#include <iostream>
using namespace std;
```

## 測試用的 Class

```cpp
class Foo {
public:
    Foo(int id) : id(id) {                         // default constructor
        cout << "<" << id << ">default constructor" << endl;
    };
    ~Foo() {                                       // destructor
        cout << "<" << id << ">destructor" << endl;
    }
    Foo(const Foo &other) : id(other.id + 1) {     // copy constructor
        cout << "<" << id << ">copy constructor" << endl;
    }
    Foo &operator=(const Foo &other) {             // copy-assignment operator
        id = other.id;
        cout << "<" << id << ">copy-assignment operator" << endl;
        return *this;
    }

    int id;
};
```

## default constructor

```cpp
int main() {
    Foo f1(1);
}
// <1>default constructor
// <1>destructor
```

## copy constructor

```cpp
int main() {
    Foo f1(1);
    Foo f2(f1);
}
// <1>default constructor
// <2>copy constructor
// <2>destructor
// <1>destructor
```

```cpp
int main() {
    Foo f1(1);
    Foo f2 = f1;
}
// <1>default constructor
// <2>copy constructor
// <2>destructor
// <1>destructor
```

## default constructor 加 copy constructor

```cpp
int main() {
    Foo f1 = Foo(1);
    cout << f1.id << endl;
}
// <1>default constructor
// <2>copy constructor
// <1>destructor
// 2
// <2>destructor
```

* `Foo(1)` 創造了一個 id 為 1 的中間值，這個中間值沒有 bind 到任何變數名稱，而 f1 藉由複製建構子複製了那個中間值，所以 f1 的 id 為 2。
* 在前面的例子裡，有 bind 到變數名稱的 object 會自動在離開 scope 後解構，但此例中的中間值 `Foo(1)`，在執行完複製建構子後就解構了。

```cpp
int main() {
    Foo f1(1);
    Foo f2 = Foo(f1);
    cout << f2.id << endl;
}
// <1>default constructor
// <2>copy constructor
// <3>copy constructor
// <2>destructor
// 3
// <3>destructor
// <1>destructor
```

* 跟前一個例子一樣，`Foo(f1)` 創造了一個 id 為 2 的中間值，這個中間值沒有 bind 到任何變數名稱，而 f2 藉由複製建構子複製了那個中間值，所以 f2 的 id 為 3。
* 此例中的中間值 `Foo(f1)`，在執行完複製建構子後就解構了。

## copy-assignment operator

```cpp
int main() {
    Foo f1(1);
    Foo f2(2);
    f2 = f1;
    cout << f2.id << endl;
}
// <1>default constructor
// <2>default constructor
// <1>copy-assignment operator
// 1
// <1>destructor
// <1>destructor
```

## 指標

指標跟上面提到的情況沒什麼不同。

```cpp
int main() {
    Foo *f1 = new Foo(1);
}
// <1>default constructor
```

```cpp
int main() {
    Foo *f1 = new Foo(1);
    delete f1;
}
// <1>default constructor
// <1>destructor
```

```cpp
int main() {
    Foo f1(1);
    Foo *f2 = new Foo(f1);
}
// <1>default constructor
// <2>copy constructor
// <1>destructor
```

## 函數（傳值呼叫）

```cpp
Foo FooOutOnly() { return Foo(0); }

int main() {
    FooOutOnly();
}
// <0>default constructor
// <1>copy constructor
// <0>destructor
// <1>destructor
```

```cpp
Foo FooOutOnly() { return Foo(0); }

int main() {
    Foo f1 = FooOutOnly();
    cout << f1.id << endl;
}
// <0>default constructor
// <1>copy constructor
// <0>destructor
// <2>copy constructor
// <1>destructor
// 2
// <2>destructor
```

```cpp
void FooInOnly(Foo f) {}

int main() {
    Foo f1(1);
    FooInOnly(f1);
}
// <1>default constructor
// <2>copy constructor
// <2>destructor
// <1>destructor
```

```cpp
void FooInOnly(Foo f) {}

int main() {
    FooInOnly(Foo(1));
}
// <1>default constructor
// <2>copy constructor
// <2>destructor
// <1>destructor
```

```cpp
Foo FooInOut(Foo f) { return Foo(f.id + 1); }

int main() {
    Foo f1(1);
    FooInOut(f1);
}
// <1>default constructor
// <2>copy constructor
// <3>default constructor
// <4>copy constructor
// <3>destructor
// <4>destructor
// <2>destructor
// <1>destructor
```

## 函數（傳參考呼叫）

```cpp
void FooInOnly(Foo &f) {}

int main() {
    Foo f1(1);
    FooInOnly(f1);
}
// <1>default constructor
// <1>destructor
```

```cpp
void FooInOnly(const Foo &f) {}

int main() {
    Foo f1(1);
    FooInOnly(f1);
}
// <1>default constructor
// <1>destructor
```

```cpp
void FooInOnly(Foo &f) {}

int main() {
    // FooInOnly(Foo(1));    // 非常數參考的初始值必須是左值
}
// (無法編譯)
```

```cpp
void FooInOnly(const Foo &f) {}

int main() {
    FooInOnly(Foo(1));
}
// <1>default constructor
// <1>destructor
```