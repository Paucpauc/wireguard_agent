FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install --no-install-recommends -y software-properties-common build-essential dkms iproute2 && \
    add-apt-repository ppa:wireguard/wireguard && \
    apt-get install --no-install-recommends -y wireguard-dkms wireguard-tools wireguard python3-requests && \
    apt-get clean
COPY ./run.sh /bin/
COPY ./wg_agent.py /bin/
ENV IFACE=wg0
ENV PYTHONUNBUFFERED=1
CMD ["run.sh"]
VOLUME /mnt/
