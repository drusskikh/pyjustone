#!/usr/bin/env python
import re
import argparse

import mididings
from mididings import *


class FormatError(Exception):
    pass


class ScalaParser(object):
    def __init__(self, path):
        self.path = path

    @staticmethod
    def _to_float(string):
        match = re.findall('[0-9]+', string)
        if len(match) != 2:
            raise FormatError
        print match
        # log (n/p) x 1200/log 2 

    def parse(self):
        f = open(self.path, 'r')
        lines_w_comments = f.readlines()
        lines = []
        for line in lines_w_comments:
            if line[0] != '!':
                lines.append(line)

        print lines[0]

        if int(lines[1]) != 12:
            raise FormatError
        if int(lines[1]) != len(lines) - 2:
            raise FormatError

        lines.pop(0)
        lines.pop(0)
        for element in lines:
            pos = re.search('[0-9./]+', element)
            print [(pos.group())]

        
        ScalaParser._to_float("5/4")


class Note(object):
    def __init__(self, note, channel):
        self.note = note
        self.channel = channel


class JusTone(object):
    count = 0
    input_channel = 1
    first_output_channel = 1
    polyphony = 4
    pitich_range = 500
    pitch = [100, 100, 50, 50, 100, 100, 50, 50, 100, 100, 50, 50]
    notes= []

    @staticmethod
    def find_note(note):
        channel_list = []
        index_list = []
        for element, index in zip(JusTone.notes, xrange(len(JusTone.notes))):
            if element.note == note:
                channel_list.append(element.channel)
            index_list.append(index)
        for index in index_list:
            JusTone.notes.pop(index)
        return channel_list

    @staticmethod
    def just_tone(event):
        evt = []
        if event.channel == JusTone.input_channel:
            if event.type == NOTEON:
                note = event.note % 12
                noteon = mididings.event.MidiEvent(NOTEON, 1,
                          JusTone.first_output_channel + JusTone.count,
                          event.note, event.velocity)
                pitchbend = mididings.event.MidiEvent(PITCHBEND, 1,
                             JusTone.first_output_channel + JusTone.count, 0,
                             JusTone.pitch[note])

                JusTone.notes.append(
                 Note(event.note, JusTone.first_output_channel + JusTone.count))

                JusTone.count += 1
                if JusTone.count >= JusTone.polyphony:
                    JusTone.count = 0
                
                evt.append(pitchbend)
                evt.append(noteon)
                return evt

            if event.type == NOTEOFF:
                noteoff = []
                channel_list = JusTone.find_note(event.note)
                for element in channel_list:
                    noteoff.append(mididings.event.MidiEvent(NOTEOFF, 1,
                                                        element, event.note, 0))
                return noteoff

            return event


if __name__ == '__main__':
#    config(client_name='PyJusTone', backend = 'alsa')
#    JusTone.pitch = [20, 20, 30, 30, 20, 20, 30, 30, 20, 20, 30, 30]
#    run(Process(JusTone.just_tone))
    parser = ScalaParser('12-19.scl')
    parser.parse()

