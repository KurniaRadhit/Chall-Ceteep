#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void win(void) {
    puts("Selamat! Ini flag kamu:");
    system("/bin/cat /flag.txt");
}

void vuln(void) {
    char nama[64];
    char username[72];

    memset(nama, 0, sizeof(nama));
    memset(username, 0, sizeof(username));

    // --- Bug #1: format string vulnerability ---
    printf("Sebutkan nama lengkapmu: ");
    int n = read(0, nama, sizeof(nama) - 1);
    if (n > 0) nama[n - 1 < 0 ? 0 : n - 1] = 0;

    printf("Halo, ");
    printf(nama);           // <-- input user dipakai langsung sebagai format string
    printf("\n");

    // --- Bug #2: stack buffer overflow, dilindungi stack canary ---
    printf("Sebutkan username ctfmu: ");
    read(0, username, 200); // username hanya 72 byte -> overflow sampai nimpa canary & return address

    puts("Terima kasih, sampai jumpa!");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    vuln();
    return 0;
}
