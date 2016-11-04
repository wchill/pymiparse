import re
from .exceptions import *
from collections import OrderedDict

__author__ = 'Eric Ahn (ericahn3@illinois.edu)'
__license__ = 'MIT'
__version__ = '0.1.2'


def parse(text_log):
    logs = re.split(r'General[^\S\n]*(?:#\d+?)*\r?\n', text_log)[1:]
    mediainfos = []
    for log in logs:
        mediainfos.append(MediaInfoLog('General\n' + log))
    return mediainfos


def parse_from_file(f):
    return parse(f.read())


class MediaInfoLog(object):

    def __init__(self, text_log):
        self._general = None
        self._audio_tracks = []
        self._video_tracks = []
        self._subtitle_tracks = []
        self._menus = OrderedDict()

        section_regex = re.compile(r'^((general|video|audio|text|menu)\s*(?:#(\d+))?)$', re.IGNORECASE)
        line_split_regex = re.compile(r'\s+:\s*')

        lines = text_log.splitlines()
        section_type = None
        working_set = None

        def add_working_set(current_type, current_set):
            if current_type is not None:
                if current_type == 'General':
                    self._general = current_set
                elif current_type == 'Video':
                    self._video_tracks.append(current_set)
                elif current_type == 'Audio':
                    self._audio_tracks.append(current_set)
                elif current_type == 'Text':
                    self._subtitle_tracks.append(current_set)
                elif current_type == 'Menu':
                    self._menus = current_set

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                add_working_set(section_type, working_set)
                section_type = None
                continue

            match = section_regex.match(line)

            if match:
                add_working_set(section_type, working_set)

                section_type = match.group(1)

                working_set = OrderedDict()
            elif section_type:
                splitted_field = line_split_regex.split(line)
                if len(splitted_field) == 1:
                    continue
                field_name = splitted_field[0].strip()
                field_value = splitted_field[1].strip()
                working_set[field_name] = field_value

        add_working_set(section_type, working_set)

        if self._general is None:
            raise InvalidMediaInfoException('No MediaInfo found.')

    @property
    def general(self):
        return self._general

    @property
    def audio_tracks(self):
        return self._audio_tracks

    @property
    def video_tracks(self):
        return self._video_tracks

    @property
    def subtitle_tracks(self):
        return self._subtitle_tracks

    @property
    def menus(self):
        return self._menus

    def get_filename(self):
        if 'Complete name' not in self.general:
            raise UnknownFieldException('No filename provided in MediaInfo.')

        match = re.match(r'(?:.*(?:\\|/))?(.+)', self.general['Complete name'])
        if match is None:
            raise UnknownFieldException('No filename provided in MediaInfo.')

        return match.group(1)

    def get_container(self):
        if 'Complete name' not in self.general:
            raise UnknownFieldException('No filename provided in MediaInfo.')

        match = re.match(r'.*\.(.+)', self.general['Complete name'])
        if match is None:
            raise UnknownFieldException('No filename provided in MediaInfo.')

        return match.group(1).upper()

    def get_primary_audio_codec(self):
        if len(self.audio_tracks) == 0:
            raise NoTrackException('No audio tracks in file.')

        audio = self.audio_tracks[0]
        codec = audio.get('Format')
        profile = audio.get('Format profile')

        if codec == 'MPEG Audio':
            if profile == 'Layer 3':
                return 'MP3'
            elif profile == 'Layer 2':
                return 'MP2'

        elif 'TrueHD' in codec:
            return 'TrueHD'

        elif codec == 'PCM':
            return 'LPCM'

        elif codec == 'FLAC':
            return 'FLAC'

        elif codec == 'DTS':
            if profile == 'MA / Core':
                return 'DTS-HD MA'
            else:
                return 'DTS'

        elif 'AC-3' in codec:
            return 'DD'

        elif codec == 'AAC':
            return 'AAC'

        raise UnknownCodecException('Unknown audio codec {}.'.format(codec))

    def get_primary_audio_channels(self):
        if len(self.audio_tracks) == 0:
            raise NoTrackException('No audio tracks in file.')

        audio = self.audio_tracks[0]

        channel_values = [audio.get('Channel(s)_Original'), audio.get('Channel(s)'), audio.get('Channel count')]
        channel_str = next((item for item in channel_values if item is not None), '')
        num_channels_match = re.match(r'(\d+) channels?', channel_str)
        if num_channels_match is not None:
            num_channels = int(num_channels_match.group(1))
        else:
            num_channels = 0

        channel_map = {
            1: '1.0',
            2: '2.0',
            3: '2.1',
            6: '5.1',
            8: '7.1'
        }

        return channel_map.get(num_channels)

    def get_audio_languages(self):
        if len(self.audio_tracks) == 0:
            raise NoTrackException('No audio tracks in file.')

        languages = set()
        for track in self.audio_tracks:
            if 'Language' in track:
                languages.add(track.get('Language'))
        return list(languages)

    def get_primary_video_codec(self):
        if len(self.video_tracks) == 0:
            raise NoTrackException('No video tracks in file.')

        video = self.video_tracks[0]

        codec = video.get('Format')

        if codec == 'AVC':
            return 'H.264'

        elif codec in ['HEVC', 'hvc1', 'hev1']:
            return 'H.265'

        elif codec == 'MPEG-4 Visual':
            writing_library = video.get('Writing library')
            codec_id = video.get('Codec ID')
            codec_id_hint = video.get('Codec ID/Hint')

            if writing_library:
                if 'xvid' in writing_library.lower():
                    return 'XviD'
                elif 'divx' in writing_library.lower():
                    return 'DivX'

            if codec_id:
                if 'xvid' in codec_id.lower():
                    return 'XviD'
                elif 'divx' in codec_id.lower():
                    return 'DivX'

            if codec_id_hint:
                if 'xvid' in codec_id_hint.lower():
                    return 'XviD'
                elif 'divx' in codec_id_hint.lower():
                    return 'DivX'

        elif codec == 'MPEG Video':
            format_version = video.get('Format version')
            if format_version == 'Version 1':
                return 'MPEG'
            elif format_version == 'Version 2':
                return 'MPEG2'

        elif codec == 'VC-1':
            return 'VC-1'

        raise UnknownCodecException('Unknown video codec {}.'.format(codec))

    def get_primary_video_bit_depth(self):
        if len(self.video_tracks) == 0:
            raise NoTrackException('No video tracks in file.')

        bit_depth = self.video_tracks[0].get('Bit depth')
        if bit_depth is None:
            raise UnknownFieldException('No bit depth field in Mediainfo.')

        return int(re.search(r'(\d+)', bit_depth).group(1))

    def get_subtitle_languages(self):
        if len(self.subtitle_tracks) == 0:
            raise NoTrackException('No subtitle tracks in file.')

        languages = set()
        for track in self.subtitle_tracks:
            if 'Language' in track:
                languages.add(track.get('Language'))
        return list(languages)

    def is_primary_video_interlaced(self):
        if len(self.video_tracks) == 0:
            raise NoTrackException('No video tracks in file.')

        video = self.video_tracks[0]
        scan_type = video.get('Scan type')
        store_method = video.get('Scan type, store method')

        return scan_type == 'Interlaced' or scan_type == 'MBAFF' or store_method == 'Interleaved fields'
