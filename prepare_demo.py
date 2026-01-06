import torchaudio
import os
import pandas as pd
import random

def prepare_samples(
    root='~/test-clean',
    run_id='f821282878',
    prefix='gold',
    prompt_length=3,
    min_secs=4,
    max_secs=10,
    save_gt=False,
):
    try:
        transcription_file = open(os.path.join(root, 'transcripts_bs5.txt'), 'r')
    except:
        transcription_file = open(os.path.join(root, 'transcripts_bs10.txt'), 'r')
    
    # collect test utt
    test_file = open(os.path.join('demo.txt'), 'r')
    test_utt = {}
    for i, line in enumerate(test_file.readlines()):
        test_utt[line[:-1]] = i
    save_path = f"test_samples/{run_id}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # collect audio samples
    pairs = []
    for line in transcription_file.readlines():
        id_ = line.split()[0]
        secs = float(line.split()[1])
        text = ' '.join(line.split()[2:])

        if secs < min_secs or secs > max_secs:
            print(secs)
            continue

        if text in test_utt.keys():
            print(test_utt[text])
            ref_path = f"{save_path}/ref_{test_utt[text]}.flac"
            gt_path = f"{save_path}/gt_{test_utt[text]}.flac"
            if save_gt:
                audio_file = f"{root}/gold-{id_}.wav"
                audio, sample_rate = torchaudio.load(audio_file)
                wav_length = prompt_length * sample_rate
                reference = audio[:, :wav_length]
                torchaudio.save(ref_path, reference, sample_rate=16000)
                sample = audio
                torchaudio.save(gt_path, sample, sample_rate=16000)

            # load prompt from gt
            audio_file = f"{root}/{prefix}-{id_}.wav"
            audio, sample_rate = torchaudio.load(audio_file)
            sample = audio
            sample_path = f"{save_path}/sample_{test_utt[text]}.flac"
            torchaudio.save(sample_path, sample, sample_rate=16000)
            pairs.append([text, ref_path, gt_path, sample_path])
    return pairs


# codec
path1 = "./results/test-clean/f768407035_checkpoint208.pt_k60_p0.9/"
pairs1 = prepare_samples(
    root=path1,
    run_id="f768407035",
    prefix="ar-concat",
    save_gt=True
)
pairs1.sort()

# dlmel-lm
path2 = "./results/test-clean/f821282878_checkpoint165.pt_k60_p0.9/"
pairs2 = prepare_samples(
    root=path2,
    run_id="f821282878",
    prefix="ar-concat"
)
pairs2.sort()
for i in range(len(pairs2)):
    # replace gt to VMel-LM
    pairs1[i].append(pairs2[i][-1])

# joint
path3 = "./results/test-clean/f831930970_checkpoint254.pt_k60_p0.9/"
pairs3 = prepare_samples(
    root=path3,
    run_id="f831930970",
    prefix="ar-concat"
)
pairs3.sort()
for i in range(len(pairs2)):
    pairs1[i].append(pairs3[i][-1])

# save melle
prepare_samples(
    root="./results/test-clean/f789493951_checkpoint757.pt_k60_p0.9/",
    run_id="f789493951",
    prefix="ar-concat"
)
# save repetition
prepare_samples(
    root="./results/test-clean/f821282878_checkpoint165.pt_k60_p0.9_penalty0//",
    run_id="f821282878_penalty0",
    prefix="ar-concat"
)

# make dir for tests
import shutil

#pairs = []
#with open("audio_pairs-1.csv") as f:
#    for line in f.readlines():
#        pairs.append(line.split(','))
#        pairs[-1][-1] = pairs[-1][-1][:-1]
#        print(pairs)

for i in range(len(pairs1)):
    path = f"demo/test-{i+1}"
    if not os.path.exists(path):
        os.makedirs(path)
    src = pairs1[i][1]
    dst = f"{path}/ref.flac"
    shutil.copyfile(src, dst)

    src = pairs1[i][2]
    dst = f"{path}/gt.flac"
    shutil.copyfile(src, dst)

    src = pairs1[i][3]
    dst = f"{path}/f768407035.flac"
    shutil.copyfile(src, dst)

    src = pairs1[i][4]
    dst = f"{path}/f821282878.flac"
    shutil.copyfile(src, dst)

    src = pairs1[i][5]
    dst = f"{path}/f831930970.flac"
    shutil.copyfile(src, dst)
    
# Create a DataFrame with two columns
df = pd.DataFrame(
    pairs1, 
    columns=['text', 'Reference', 'GT', 'f768407035', 'f821282878', 'f831930970']
)
# Save to Excel
df.to_csv('demo.csv', index=False)
