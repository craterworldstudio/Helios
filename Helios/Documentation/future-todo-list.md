# Helios Compiler TODO

## Parser

### High Priority
- [ ] Implement binary operator precedence ladder
- [ ] Complete expression parser
- [ ] Implement all statement parsers
- [ ] Parse blocks (`{ ... }`)
- [ ] Parse TASK and SubTASK signatures
- [ ] Parse imports/exports
- [ ] Parse structs
- [ ] Parse enums

---

## Type System

### Future
- [ ] Add `type_reference()` parser.
    Instead of accepting only `TT_DATATYPE` after `as`, parse complete type references.

    Planned supported syntax:

    ```hls
    value as i32
    value as bool
    value as v3

    value as PlayerData
    value as Physics.Transform
    value as su.types.struct
    value as Group:StructName
    ```

- [ ] Support user-defined types in variable declarations.
- [ ] Support namespaced types.
- [ ] Support imported type aliases.

---

## Semantic Analysis

- [ ] Symbol Table
- [ ] Scope management
- [ ] Type checking
- [ ] Cast validation
- [ ] Struct member validation
- [ ] Enum validation

---

## AST

- [ ] AST Pretty Printer
- [ ] AST Visualizer
- [ ] AST serialization (optional)

---

## Compiler

- [ ] Intermediate Representation (HIR)
- [ ] Optimizer
- [ ] Code Generation
- [ ] Binary Output

---

## Language Features

- [ ] Generic containers
- [ ] Anonymous structs (optional)
- [ ] Compile-time constants
- [ ] Constant folding
- [ ] Dead code elimination

---

## Tooling

- [ ] LSP
- [ ] Syntax highlighting
- [ ] Formatter
- [ ] Documentation generator


## Deferred Features

- [ ] Nothing really good right now