import librosa
import csv
from pydub import AudioSegment
from pydub import silence
import numpy

audio_file = './RellBattle_concatenated/RellBattle_concatenated.wav'

silences = []
silence_counter = 0
with open('silences.csv', 'r') as csvfile:
    silence_reader = csv.reader(csvfile)
    for row in silence_reader:
        silences.append(float(row[0]))

audio, sampling_rate = librosa.load(audio_file)
intervals = librosa.effects.split(audio, top_db=40)
print len(intervals)

print librosa.core.get_duration(audio)
sound_file = AudioSegment.from_wav(audio_file)
print len(sound_file)


#tagging each utterances as setup or punchline
def interval_to_ms(interval):
    interval_ms = librosa.core.frames_to_time(librosa.core.samples_to_frames(interval))
    return interval_ms[0]*1000.0

tagged_utterances = []

# interval_stats = []
# for r in range(0, len(intervals)):
#     interval_stats.append(interval_to_ms(intervals[r][1]) - interval_to_ms(intervals[r][0]))
#     #tagged_utterances.append([interval_to_ms(intervals[r][0]), interval_to_ms(intervals[r][1]), 'setup'])

# print numpy.mean(interval_stats)
# print numpy.std(interval_stats)

for r in range(0, len(intervals)):
    tagged_utterances.append([interval_to_ms(intervals[r][0]), interval_to_ms(intervals[r][1]), 'setup'])

silence_counter = 0
for i, t in enumerate(intervals):
    start = librosa.core.frames_to_time(librosa.core.samples_to_frames(t[0]))
    end = librosa.core.frames_to_time(librosa.core.samples_to_frames(t[1]))
    if start > silences[silence_counter]:
        silence_counter = silence_counter + 1
        tagged_utterances[i-1] = [interval_to_ms(intervals[i-1][0]), interval_to_ms(intervals[i-1][1]), 'punchline']
    if i == len(intervals)-1:
        tagged_utterances[i] = [interval_to_ms(intervals[i][0]), interval_to_ms(intervals[i][1]), 'punchline']

#SAVE TAGS AND UTTERANCE FILES
tag_file = open('RellBattletags.csv', 'w')

#Process each chunk per requirements
for x, tu in enumerate(tagged_utterances):
    print(tu)
    new_file = sound_file[int(tu[0]):int(tu[1])]
    tag_file.write("RellBattle_utterance{0}.wav".format(x)+','+ str(tu[2])+'\n')
    #Export audio chunk with new bitrate
    print("exporting RellBattle_utterance{0}.wav".format(x))
    new_file.export("./RellBattle_utterances/RellBattle{0}.wav".format(x), bitrate='192k', format="wav")
tag_file.close()




