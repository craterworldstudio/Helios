# Helios Language Syntax Specification (Current Draft)

> **Version:** Draft 0.1
> **Status:** Based on current language design discussions.

---

# General Philosophy

- Case Sensitive.
- Explicit over implicit.
- Designed for distributed game servers.
- Runtime is built around Groups and Tasks.
- `create` only declares variables.
- `set` only modifies existing variables.
- Every executable statement must exist inside a `TASK` or `SubTASK` where required.

---

# File Types

```hls
type MASTER
type SRC
type WORKER
type WORKER_C
type SWORKER
type SLAVE
type SLAVE_C
type CFG
```

---

## MASTER

May contain

- import
- group
- categories
- type declaration

Cannot contain

- export blocks
- TASK
- SubTASK

---

## SRC

May contain

- import
- export
- categories
- group
- General Purpose Code

---

## WORKER / WORKER_C / SWORKER / SLAVE / SLAVE_C

May contain

- import
- export
- group
- TASK
- SubTASK

Nothing executable is allowed outside TASK/SubTASK.

---

# Imports

Standard import

```hls
import math
```

Alias

```hls
import systemutils as su
import objects as obj
```

---

# Exports

Exports define a group's public API.

Example

```hls
export (
    CheckCollision as bool,
    CollisionCount as i32
)
```

Only exported members are visible outside the group.

MASTER files cannot export.

---

# Groups

Every source file / module contains one group.

```hls
group Collision
```

Groups cannot be nested or edited at runtime.

---

# TASK

Syntax

```hls
TASK GroupName:TaskName(arguments...) -> ReturnType {

}
```

Example

```hls
TASK Collision:Initialize(poolmanager) -> null {

}
```

Rules

- Task name MUST include the owning group.
- Executable code exists here.

---

# SubTASK

Syntax

```hls
SubTASK GroupName:TaskName(arguments...) -> ReturnType {

}
```

Example

```hls
SubTASK Collision:CheckCollision(EntityListId, PlayerId) -> bool {

}
```

Rules

- Must include owning group.
- Can be exported.
- Can be called from other SubTask and Tasks.

---

# Calling Tasks

Calls use namespace/group syntax.

```hls
Collision:CheckCollision(player, entities)
```

Not

```hls
Collision.CheckCollision()
```

---

# Variables

Declaration

```hls
create i32 score = 0
```

Update

```hls
set score 100
```

Rules

- `create` only declares.
- `set` only updates.

---

# Primitive Types

Unsigned Integers

```text
u8
u16
u32
u64
```

Signed Integers

```text
i8
i16
i32
i64
```

Floating Point

```text
f16
f32
f64

f16p
f32p
f64p
```

Binary

```text
b8
b16
b32
```

Hex

```text
h1
h2
h4
```

Boolean

```text
bool
```

Strings

```text
s32
s64
s128
```

Large Strings

```text
str
```

Vectors

```text
v2
v3
v4
```

Runtime Objects

```text
process
task
subtask
```

---

# Numeric Literals

Integer

```hls
123
```

Float

```hls
84.56
```

Binary

```hls
0b101010
```

Hex

```hls
0xFFA012
```

Illegal

```hls
123abc
```

Identifier cannot immediately follow a number.

---

# Strings

```hls
"Hello"
'Hello'
```

Escape sequences

```text
\n
\t
\r
```

---

# Boolean

```hls
true
false
```

---

# Null

```hls
null
```

---

# Struct

Syntax

```hls
struct GroupName:StructName {

    "Health": i32 <- 100,
    "Name": str <- "Player",
    "Velocity": v3 <- null

}
```

Null fields require explicit typing before assignment.

```hls
set GroupName:StructName.Velocity v3
```

---

# Enum

Syntax

```hls
enum Weapon : str {

    "Sword",
    "Bow",
    "Gun"

}
```

Enum values must match the declared enum type.

---

# Type Casting

```hls
player.position as v3
```

`as` converts or interprets data as another type.

---

# Import Alias

```hls
import systemutils as su
```

---

# Export Alias

```hls
export (

    Position as v3,
    CheckCollision as bool

)
```

---

# Runtime Pool Example

```hls
clutch playerData = pm_access.get(PlayerId) as su.types.struct
```

---

# Member Access

```hls
player.position
player.velocity
```

`.` accesses members.

---

# Namespace Access

```hls
Collision:Initialize()
Collision:CheckCollision()
Player:Data
Player:Data.Position
```

`:` represents ownership or namespace.

---

# Control Flow

If

```hls
if (condition) {

}
else {

}
```

While

```hls
while (condition) {

}
```

For

```hls
for (id <- Entity; id++) {

}
```

Switch

```hls
switch category_name
```

---

# Categories

Categories divide code into logical sections.

```hls
cat Physics {
    ...
}
```

Used for organization.

Groups cannot be nested.

---

# Return

```hls
return value
```

---

# Break

```hls
break
```

---

# Skip

```hls
skip
```

---

# Synchronization

Hold

```hls
hold resource
```

Clutch

```hls
clutch resource
```

Used for synchronization primitives.

---

# Operators

Assignment

```text
=
+=
-=
*=
/=
%=
```

Arithmetic

```text
+
-
*
/
//
%
```

Comparison

```text
==
!=
<<
>>
<=
>=
```

Bit Shift

```text
<<=
>>=
<<<
>>>
```

Logical

```text
&&
||
!!
!&
!|
^
!^
```

Increment

```text
++
--
```

Arrow

```text
->
<-
```

---

# Visibility Rules

Groups expose only exported members.

Everything else is private.

---

# Language Rules

1. Language is case sensitive.

2. Variables are created only using `create`.

3. Variables are updated only using `set`.

4. TASK names must include their owning group.

5. SubTASK names must include their owning group.

6. Groups cannot be nested.

7. Only exported members are visible outside a group.

8. MASTER files cannot export.

9. Worker/Slave files cannot contain executable code outside TASK/SubTASK.

10. `:` is namespace/ownership resolution.

11. `.` is member access.

12. `123abc` is an invalid numeric literal.

13. `as` is used for aliasing and type casting.

14. Struct fields initialized to `null` require explicit type assignment before use.

---
