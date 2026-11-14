FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash chall

WORKDIR /chall
COPY chall.c .

RUN gcc -fstack-protector-all -no-pie -z noexecstack -z relro -z now -O0 \
    -o chall chall.c && \
    chown root:root chall && chmod 755 chall

ARG FLAG=LKS{e92b7a4c1d8f6035a9c2e7b4f16d8305}
RUN echo "$FLAG" > /flag.txt && chown chall:chall /flag.txt && chmod 400 /flag.txt

EXPOSE 9999
USER chall

CMD ["socat", "-T60", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:/chall/chall,stderr"]
