# 📘 PSEUDOCODE STANDARD

This document defines the syntax and structure of the language.
It will keep updating as new features are added.

---

## 1. Variables

### Declaration & Assignment

**Syntax:**
```text
SET <variable> TO <expression>
```

**Example:**
```text
SET x TO 10
SET y TO x + 5
```

### Input

**Syntax:**
```text
INPUT <variable>
```

**Example:**
```text
INPUT age
```

### Output

**Syntax:**
```text
PRINT <expression>
```

**Example:**
```text
PRINT x
PRINT x + y
```

---

## 2. Conditionals

### If–Else Statement

**Syntax:**
```text
IF <condition> THEN
    <statements>
ELSE
    <statements>
END
```

**Example:**
```text
SET x TO 10

IF x > 5 THEN
    PRINT x
ELSE
    PRINT 0
END
```

>  The `ELSE` branch is optional.
> *(If-Else ladder will be added later)*

---

## 3. Loops

### While Loop

**Syntax:**
```text
WHILE <condition>
    <statements>
END
```

**Example:**
```text
SET i TO 0

WHILE i < 5
    PRINT i
    SET i TO i + 1
END
```

### For Loop

**Syntax:**
```text
FOR <variable> FROM <start> TO <end> DO
    <statements>
END
```

**Example:**
```text
FOR i FROM 0 TO 4 DO
    PRINT i
END
```

### For Loop with Step

**Syntax:**
```text
FOR <variable> FROM <start> TO <end> STEP <step> DO
    <statements>
END
```

**Example:**
```text
FOR i FROM 0 TO 20 STEP 2 DO
    PRINT i
END
```

>  Both ends are **inclusive** — `FROM 0 TO 4` iterates i = 0, 1, 2, 3, 4.
> Step defaults to `1` when omitted.

---

## 4. Functions

### Definition

**Syntax:**
```text
FUNCTION <name>(<param1>, <param2>, ...)
    <statements>
    RETURN <expression>
END
```

**Example:**
```text
FUNCTION add(a, b)
    RETURN a + b
END
```

### Call as Statement

**Syntax:**
```text
CALL <name>(<arg1>, <arg2>, ...)
```

**Example:**
```text
CALL add(3, 7)
```

### Call as Expression

**Syntax:**
```text
SET <variable> TO <name>(<arg1>, <arg2>, ...)
```

**Example:**
```text
SET result TO add(3, 7)
PRINT result
```

---

## 5. Arrays

### Declare

**Syntax:**
```text
ARRAY <name>[<size>]
```

**Example:**
```text
ARRAY nums[5]
```

### Write Element

**Syntax:**
```text
SET <name>[<index>] TO <expression>
```

**Example:**
```text
SET nums[0] TO 42
```

### Read Element

**Syntax:**
```text
PRINT <name>[<index>]
```

**Example:**
```text
PRINT nums[0]
```

> 💡 Arrays are zero-indexed and initialised to `[0, 0, …, 0]` on declaration.

---

## 6. Operators

### Arithmetic

| Symbol | Meaning        | Example      |
|--------|----------------|--------------|
| `+`    | Addition       | `x + y`      |
| `-`    | Subtraction    | `x - y`      |
| `*`    | Multiplication | `x * y`      |
| `/`    | Division       | `x / y`      |
| `%`    | Modulo         | `x % 2`      |

### Comparison

| Symbol | Meaning          | Example      |
|--------|------------------|--------------|
| `==`   | Equal            | `x == y`     |
| `!=`   | Not equal        | `x != y`     |
| `>`    | Greater than     | `x > 0`      |
| `<`    | Less than        | `x < 10`     |
| `>=`   | Greater or equal | `x >= 5`     |
| `<=`   | Less or equal    | `x <= 5`     |
| `===`  | Type assignment  | `x === y`    |

---

##  7. Complete Example

```text
// Define a helper function
FUNCTION add(a, b)
    RETURN a + b
END

// Populate an array with even numbers
ARRAY nums[5]
FOR i FROM 0 TO 4 DO
    SET nums[i] TO i * 2
END

// Print each element
FOR i FROM 0 TO 4 DO
    PRINT nums[i]
END

// Call function and print result
SET result TO add(3, 7)
PRINT result
```

**Output:**
```
0
2
4
6
8
10
```

---

*Pseudocode Standard · v1.0 · Updated April 2026 · Compiles to Python 3 via `main.py`*
