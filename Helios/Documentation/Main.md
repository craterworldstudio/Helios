Compiled language.
Statically type. Threaded.

Files will be divided into groups and auth types.
Valid Group Types: A-Z, a-z, _
Master or main group must begin with MG_{identifier}

Auth Types or Execution Roles: MASTER, WORKER, SLAVE, WORKER_C, SLAVE_C, CFG, SWORKER

MASTER: the main file the compiler will look for when starting to compile and main executable. Runs for lifetime.

WORKER: like packages and namespace groups, these are functions or thread or anything which can be called by MASTER. These, takes no input arguments and Runs for lifetime once called and cannot be terminated safely unless killed by MASTER explicitly or under FATAL error. If there is no more code to run, they will flag themselves as SCARCE and loop back the code.

SLAVE: same as workers except they are short lived tasks that terminate themselves after execution unless specified by WORKER to not to. Single tasked threads alike. They take no input.

WORKER_C : same as WORKER except they take arguments and submit back the argument to other WORKER_C(s) to forward the argument to  SLAVE_C(s)

SLAVE_C : same as SLAVE except they take arguments and submit back the argument to other SLAVE_C(s) or SLAVE or parent WORKER.

CFG : Contains configuration and other types which may or may not change. Only affected by SWORKER.

SWORKER: or Super Worker, holds almost the same authority as MASTER and reads and edits the CFG. Limited to a set no. Which can exist which can be defined in the CFG in order to prevent exploiters from spawning SWORKERs.

Memory Model:

Each Role will have a local buffer memory defined at their creation.
MASTER -> WORKER and WORKER_C and SWORKER
WORKER -> SLAVE
WORKER_C -> SLAVE_C

After creation of the SWORKER managing the memory pool, it will separate itself from the pipeline and exist as a self sustaining unit with only a common data channel which takes a pid and creation signature for verification. Each valid submission persists for 2 requests. If a task (function) finishes without exhausting it's cap, the pool manager with revoke it's remaining request. If a pid, signature is wrong, the concerned Role will be killed. If the Role doesn't provide pid and signature, it will killed. If the ownership doesn't match rules or invalid owned-Roles ask the manager, it will be killed.


Data types:
- Unsigned int - u8, u16, u32, u64                                      = 0
- Signed - i8, i16, i32, i64                                                      = 0
- float - f16, f32, f64                                                              = 0.0
- float precise - f16p, f32p, f64p                                          = 0.0
- vector -  v2, v3, v4                                                              = {0, 0} {0, 0} {0, 0}
- ratio - r8, r16, r32                                                               = 1/1
- strings - s32, s64 str, refer to s32 -> 8 char, s64-> 16 char, str -> no limit.        = ""
- bool - true, false                                                                 = false
- DS - array, hashmap, n-ary tree, set                               = [], {}, {} 
- misc - process, generator, task, waypoint                     = nil

*f-p means half is integral portion and other half is decimal. Easily converted to ratio type.


Planned library:

- math,
- fs - filesystem
- systemutils - MASTER setup, status, flag, switch controlling, etc. idk what to add. 


Variable Declaration:

```
create x : u32 = 5 Regular Variable Declaration. 
```
*Data Type is Inferred if not mentioned. 

```
create set pi : u64 = 3.141519...
``` 


Operators:

`||| is a special operator which is used to parallel process 2 or more commands from right to left. 
`==, != << >> <= >= are the same Comparison Operations.
`+ - * / // % are the same arithmatic operators.
`.has() is a membership operator and, or not are the logical ops. 
`.is() is a identity op which compares memory location. 
`<<< and >>> are bitwise shifts, 
`&& || !! are bitwise and, or, not. 
`!& !| are Nand and Nor, and 
`^ and !^ are XOR and XNOR.

` =, +=, -=, *= /= %= &= |= <<<= >>>=  has usualshort hand assignemnt meaning.
`
`x++ and x-- are increment and decrement counters.`

Unary:
```
+x , -x , not x , !x
```


Methods / Functions :

	Master Functions:

	Worker/Slave Functions:
	
```
TASK GroupName:name ( !Only for _C variant Files ) {
}
```

