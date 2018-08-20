#SAVE AN ARRAY OF WHERE THE SILENCES ARE HERE

import os
from pydub import AudioSegment


standup_name = 'RellBattle'
audio_files = './RellBattle_laughremoved/'
output_file = './RellBattle_concatenated/RellBattle_concatenated.wav'
silences = []

second_silence = AudioSegment.silent(duration=1000)

combined_wav = second_silence

for x in range(0, len(os.listdir(audio_files))):
    audio_pathway = audio_files + standup_name + str(x) + '.wav'
    print audio_pathway
    audio = AudioSegment.from_wav(audio_pathway)
    silence_starts_at = combined_wav + audio
    minutes, seconds = str(silence_starts_at.duration_seconds/60.0).split('.')
    print seconds
    seconds = float('.'+seconds)*60.0
    print (minutes, seconds)
    # something here about when the second silence is appended
    silences.append(silence_starts_at.duration_seconds)
    combined_wav = combined_wav + audio + second_silence


combined_wav.export(os.path.join(os.path.dirname(__file__), output_file), format="wav")     
silence_file = open('silences.csv', 'w')
for s in silences:
    silence_file.write(str(s)+'\n')
silence_file.close()