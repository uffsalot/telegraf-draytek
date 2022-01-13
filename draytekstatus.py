#!/usr/bin/python3
from telnetlib import Telnet
import time
import re

username = "admin"
password = "admin"
host = '192.168.1.1'
timeout = 2

with Telnet(host, 23) as tn:
    tn.read_until(b"Account:", timeout)
    tn.write(username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ", timeout)
    tn.write(password.encode('ascii') + b"\n")
    tn.read_until(b"DrayTek> ", timeout)
    tn.write(b"vdsl status\n")
    status = tn.read_until(b"DrayTek> ", timeout)
    tn.write(b"vdsl status more\n")
    statusmore = tn.read_until(b"DrayTek> ", timeout)

    for line in status.splitlines():
        if(match := re.search('\s+DS Actual Rate\s+:\s+(\d+) bps\s+US Actual Rate\s+:\s+(\d+) bps',
                              line.decode())):
            act_rate_down = int(match.group(1))
            act_rate_up = int(match.group(2))
        if(match := re.search('\s+DS Attainable Rate\s+:\s+(\d+) bps\s+US Attainable Rate\s+:\s+(\d+) bps',
                              line.decode())):
            att_rate_down = int(match.group(1))
            att_rate_up = int(match.group(2))
        if(match := re.search('\s+DS Interleave Depth\s+:\s+(\d+)\s+US Interleave Depth\s+:\s+(\d+)\s+',
                              line.decode())):
            intl_down = int(match.group(1))
            intl_up = int(match.group(2))
        if(match := re.search('\s+NE Current Attenuation\s+:\s+(\d+)\s+dB\s+Cur SNR Margin\s+:\s+(\d+)\s+dB',
                              line.decode())):
            atten_down = int(match.group(1))
            snr_down = int(match.group(2))
        if(match := re.search('\s+Far Current Attenuation\s+:\s+(\d+)\s+dB\s+Far SNR Margin\s+:\s+(\d+)\s+dB',
                              line.decode())):
            atten_up = int(match.group(1))
            snr_up = int(match.group(2))

    for line in statusmore.splitlines():
        if(match := re.search('\s+FECS\s+:\s+(\d+)\s+(\d+) \(seconds\)', line.decode())):
            fec_down = int(match.group(1))
            fec_up = int(match.group(2))
        if(match := re.search('\s+ES\s+:\s+(\d+)\s+(\d+) \(seconds\)', line.decode())):
            es_down = int(match.group(1))
            es_up = int(match.group(2))
        if(match := re.search('\s+SES\s+:\s+(\d+)\s+(\d+) \(seconds\)', line.decode())):
            ses_down = int(match.group(1))
            ses_up = int(match.group(2))
        if(match := re.search('\s+CRC\s+:\s+(\d+)\s+(\d+)', line.decode())):
            crc_down = int(match.group(1))
            crc_up = int(match.group(2))

    es_down_total = es_down + ses_down
    es_up_total = es_up + ses_up

    print(f"vdslstats,host={host} act_rate_down={act_rate_down},act_rate_up={act_rate_up},att_rate_down={att_rate_down},att_rate_up={att_rate_up},intl_down={intl_down},intl_up={intl_up},atten_down={atten_down},snr_down={snr_down},atten_up={atten_up},snr_up={snr_up},fec_down={fec_down},fec_up={fec_up},es_down={es_down},es_up={es_up},ses_down={ses_down},ses_up={ses_up},crc_down={crc_down},crc_up={crc_up}")
    print("", end='', flush=True)
