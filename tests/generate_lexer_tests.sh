#!/usr/bin/env bash

set -e

ROOT="tests/lexer"

mkdir -p "$ROOT/valid"
mkdir -p "$ROOT/invalid"

####################################
# VALID TESTS
####################################

cat > "$ROOT/valid/01_variables.hls" << 'EOF'
create i8 age = 18
create s32 score = -145
create str name = "Helios"
create bool alive = true
EOF

cat > "$ROOT/valid/02_floats.hls" << 'EOF'
create f32 pi = 3.141592
create f64 value = .5
create f64 another = 10.
EOF

cat > "$ROOT/valid/03_binary.hls" << 'EOF'
create b8 flags = 0b10101010
create b16 mask = 0b1111000011110000
EOF

cat > "$ROOT/valid/04_hex.hls" << 'EOF'
create h2 color = 0xFF
create h4 value = 0xDEADBEEF
EOF

cat > "$ROOT/valid/05_strings.hls" << 'EOF'
create str hello = "Hello"
create str escape = "Line1\nLine2\tTabbed"
create str quote = "\"Quoted\""
EOF

cat > "$ROOT/valid/06_comments.hls" << 'EOF'
$ this is a comment $

create i8 x = 5

$
multiline
comment
$

create i8 y = 10
EOF

cat > "$ROOT/valid/07_operators.hls" << 'EOF'
if a == b:
if a != b:
if a <= b:
if a >= b:
if a << b:
if a >> b:
if a && b:
if a || b:
EOF

cat > "$ROOT/valid/08_delimiters.hls" << 'EOF'
func(a,b,c):
{
    value[5]
}
EOF

####################################
# INVALID TESTS
####################################

cat > "$ROOT/invalid/01_invalid_float.hls" << 'EOF'
create f32 pi = 1.2.3
EOF

cat > "$ROOT/invalid/02_invalid_identifier.hls" << 'EOF'
create i8 x = 123abc
EOF

cat > "$ROOT/invalid/03_unterminated_string.hls" << 'EOF'
create str s = "Hello
EOF

cat > "$ROOT/invalid/04_invalid_escape.hls" << 'EOF'
create str s = "\q"
EOF

cat > "$ROOT/invalid/05_unterminated_comment.hls" << 'EOF'
$
This comment never ends
EOF

cat > "$ROOT/invalid/06_invalid_binary.hls" << 'EOF'
create b8 bits = 0b10201
EOF

cat > "$ROOT/invalid/07_invalid_hex.hls" << 'EOF'
create h2 color = 0x12ZG
EOF

cat > "$ROOT/invalid/08_invalid_operator.hls" << 'EOF'
create i8 x = 5 >>>=
EOF

cat > "$ROOT/invalid/09_illegal_character.hls" << 'EOF'
€
EOF

cat > "$ROOT/invalid/10_invalid_decimal.hls" << 'EOF'
create f32 x = ..
EOF

echo
echo "=================================="
echo "Lexer test suite generated."
echo "=================================="
echo
echo "Valid tests:"
ls "$ROOT/valid"
echo
echo "Invalid tests:"
ls "$ROOT/invalid"