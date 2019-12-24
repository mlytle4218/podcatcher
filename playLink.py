#!/usr/bin/env python3
import sys,os 
import subprocess
import click

@click.command()
@click.argument('link')
@click.option('--record', '-r', help="File and location to record the link to")
def startup(link, record):
    if (record):
        print('record it')
        subprocess.Popen(['mpv','--no-video', '--really-quiet', link])
        subprocess.call(['pulseaudio','-D','--exit-idle-time=-1'])
        subprocess.call(['pacmd','load-module','module-virtual-sink','sink_name=v1'])
        subprocess.call(['pacmd','set-default-sink','v1'])
        subprocess.call(['pacmd','set-default-source','v1.monitor'])

        print('starting to record {}'.format(record))
        subprocess.call(['ffmpeg','-loglevel','panic','-f','pulse','-i','default', '/sound{}'.format(record)])
        print('recording of {} stopped'.format(record))
    else:
        print('playing only')
        subprocess.call(['mpv', '--no-video', link])

startup()
