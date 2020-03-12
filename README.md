# [LUCKY NUMBERS](https://gist.github.com/lucascebertin/993ef6bdd70494b74548104cd483f3c7)

Desafio simples (nivel 1) do site crackmes.one

Baixe o arquivo zipado e leia o FAQ para descobrir qual é a senha do zip.

Deixe o binário na raiz deste repositório.

IMPORTANTE: no arquivo lucky_numbers.py, o terminal configurado é o zsh, se utilizar outro, troque antes de executar.

## Pré-requisito:
- linux (ou algo compatível, foi feito e testando em um manjaro)
- python 3
- pip
  - pwn (pip install pwn)
- gdb
- gdbserver (instalado junto com o gdb)


## Informações sobre o binário:

```bash
$ file lucky_numbers
lucky_numbers: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, stripped

$ readelf -a ./lucky_numbers
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Intel 80386
  Version:                           0x1
  Entry point address:               0x804903a
  Start of program headers:          52 (bytes into file)
  Start of section headers:          8256 (bytes into file)
  Flags:                             0x0
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         3
  Size of section headers:           40 (bytes)
  Number of section headers:         5
  Section header string table index: 4

Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            00000000 000000 000000 00      0   0  0
  [ 1] .text             PROGBITS        08049000 001000 00008d 00  AX  0   0 16
  [ 2] .data             PROGBITS        0804a000 002000 000024 00  WA  0   0  4
  [ 3] .bss              NOBITS          0804a024 002024 000004 00  WA  0   0  4
  [ 4] .shstrtab         STRTAB          00000000 002024 00001c 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  p (processor specific)

There are no section groups in this file.

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  LOAD           0x000000 0x08048000 0x08048000 0x00094 0x00094 R   0x1000
  LOAD           0x001000 0x08049000 0x08049000 0x0008d 0x0008d R E 0x1000
  LOAD           0x002000 0x0804a000 0x0804a000 0x00024 0x00028 RW  0x1000

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .text 
   02     .data .bss 

There is no dynamic section in this file.

There are no relocations in this file.

The decoding of unwind sections for machine type Intel 80386 is not currently supported.

No version information found in this file.

$ strings -t d -d lucky_numbers
   8192 Lucky Numbers: Good Job !
   8218 Sorry :((
```

## Assembly extraido via objdump:

```bash
$ objdump -M intel -d ./lucky_numbers
```

```asm
08049000 <.text>:
 8049000:	b8 04 00 00 00       	mov    eax,0x4
 8049005:	bb 01 00 00 00       	mov    ebx,0x1
 804900a:	b9 1a a0 04 08       	mov    ecx,0x804a01a
 804900f:	ba 0a 00 00 00       	mov    edx,0xa
 8049014:	cd 80                	int    0x80
 8049016:	b8 01 00 00 00       	mov    eax,0x1
 804901b:	cd 80                	int    0x80
 804901d:	b8 04 00 00 00       	mov    eax,0x4
 8049022:	bb 01 00 00 00       	mov    ebx,0x1
 8049027:	b9 0f a0 04 08       	mov    ecx,0x804a00f
 804902c:	ba 0b 00 00 00       	mov    edx,0xb
 8049031:	cd 80                	int    0x80
 8049033:	b8 01 00 00 00       	mov    eax,0x1
 8049038:	cd 80                	int    0x80
 804903a:	b8 04 00 00 00       	mov    eax,0x4
 804903f:	bb 01 00 00 00       	mov    ebx,0x1
 8049044:	b9 00 a0 04 08       	mov    ecx,0x804a000
 8049049:	ba 0f 00 00 00       	mov    edx,0xf
 804904e:	cd 80                	int    0x80
 8049050:	b8 03 00 00 00       	mov    eax,0x3
 8049055:	bb 02 00 00 00       	mov    ebx,0x2
 804905a:	b9 24 a0 04 08       	mov    ecx,0x804a024
 804905f:	ba 02 00 00 00       	mov    edx,0x2
 8049064:	cd 80                	int    0x80
 8049066:	a0 24 a0 04 08       	mov    al,ds:0x804a024
 804906b:	2c 30                	sub    al,0x30
 804906d:	8a 1d 25 a0 04 08    	mov    bl,BYTE PTR ds:0x804a025
 8049073:	80 eb 30             	sub    bl,0x30
 8049076:	10 d8                	adc    al,bl
 8049078:	27                   	daa    
 8049079:	80 c3 30             	add    bl,0x30
 804907c:	3c 16                	cmp    al,0x16
 804907e:	75 80                	jne    0x8049000
 8049080:	80 fb 38             	cmp    bl,0x38
 8049083:	0f 85 77 ff ff ff    	jne    0x8049000
 8049089:	39 c0                	cmp    eax,eax
 804908b:	74 90                	je     0x804901d
```

## Ponto de entrada do binário

Através do resultado do readelf, podemos ver que a entrada do binário está em: `Entry point address: 0x804903a`

## Chamadas de [kernel](https://syscalls.kernelgrok.com/):

Sys-write:
```asm
mov    eax,0x4 # 	sys_write(unsigned int fd /*ebx*/, const char __user *buf /*ecx*/, size_t count /*edx*/);
mov    ebx,0x1
mov    ecx,0x804a01a 
mov    edx,0xa
int    0x80 
```

Sys-exit:
```asm
mov    eax,0x1 # sys_exit(int error_code /*ebx*/)
int    0x80
```

Sys-read:
```asm
mov    eax,0x3 # sys_read(unsigned int fd /*ebx*/, char __user *buf /*ecx*/, size_t count /*edx*/);
mov    ebx,0x2
mov    ecx,0x804a024
mov    edx,0x2
int    0x80
```

## Código que realmente interessa:

```asm
mov    al,ds:0x804a024            # dado o valor de entrada, extraia o primeiro digito em AL
sub    al,0x30                    # subtraia 0x30 do registrados AL
mov    bl,BYTE PTR ds:0x804a025   # dado o valor de entrada, extraia o segundo digito em BL
sub    bl,0x30                    # subtraia 0x30 do registrados BL
adc    al,bl                      # Some AL + BL e guarde em AL
daa                               # Transforme o valor (decimal) em um número hexadecimal (10 passa a ser 0x10, em decimal ficaria 16)
add    bl,0x30                    # Some 0x30 ao registrador BL
cmp    al,0x16                    # Compare AL a 0x16
jne    0x8049000                  # Se a comparação der errado, jump para falha   
cmp    bl,0x38                    # Compara BL a 0x38
jne    0x8049000                  # Se a comparação der errado, jump para falha
cmp    eax,eax                    # comparação inutil, sempre dá true (ex: 1 == 1)
je     0x804901d                  # jump para mensagem de sucesso
```

## Análise e RE:
```c
falha() { 
  print("Sorry :((").
}

sucesso() {
  print("Good Job !")
}

main () 
{
  numeros_recebido
  x = numeros_recebido_em_formato_texto[0] // Exemplo '1' -> 0x31
  x = x - 0x30 //conversão de texto para numero, '1' -> 0x31, 0x31 - 0x31 = 0x1 -> 1 

  y = numeros_recebido_em_formato_texto[1]
  y = y - 0x30 //conversão de texto para numero, '1' -> 0x31, 0x31 - 0x31 = 0x1 -> 1 

  x = x + y
  x = (hex)x // 10 -> 0x10

  y = y + 0x30

  if x != 0x16
    falha()

  if y != 0x38
    falha()

  if x == x
    sucesso()
}

/*
x = 0x31
x = 0x31 - 0x30 -> 0x1

y = 0x31
y = 0x31 - 0x30 -> 0x1

x = 2
y = y + 0x30 -> 0x31

x != 0x16
y != 0x38  //Para dar 0x38, y precisa receber '8' para virar 8 (0x38 -> 0x8 após subtração de 0x30)

Logo:
 
y = 8
x + y = 0x16
x + 0x8 = 0x16
x = 0x16 - 0x8 
x = 0x8

x = '8'
y = '8'
*/
```

## Brute force

### Brute usando pwntools: [link](lucky_numbers.py)

```bash
$ python3 ./lucky_numbers.py
Found it... 88
```

### Brute usando GDB com python: [link](lucky_numbers_gdb.py)

```bash
$ gdb
(gdb) source ./lucky_numbers_gdb.py  
Breakpoint 1 at 0x804903a
Breakpoint 2 at 0x8049066
Breakpoint 3 at 0x804907e
Breakpoint 4 at 0x8049083 

Breakpoint 1, 0x0804903a in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? () 
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? () 
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 4, 0x08049083 in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 2, 0x08049066 in ?? ()
Breakpoint 3, 0x0804907e in ?? ()
Breakpoint 4, 0x08049083 in ?? ()

Good numbers
Flag: 88
```
