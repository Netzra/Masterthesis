import time
import slab
import numpy as np
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 8001)

distance_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
distance_ids_rev = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
y_positions = np.linspace(2800, 1000, 11)
x_pos = 1000.
z_pos = 120.
distance_table = dict(zip(distance_ids, y_positions))
test_conditions = [1, 2, 4, 8, 11]

subject_ID = 'jakab'


def run_trials(seq, is_test=False):
    stage = "test" if is_test else "training"
    file = slab.ResultsFile(subject=subject_ID)
    file.write(subject_ID, tag="subject_ID")
    file.write(stage, tag="stage")
    file.write(distance_table, tag="distance_table")
    for trial in seq:
        distance_id = int(trial)
        y_pos = float(distance_table[distance_id])
        client.send_message("/ctrlUnreal/sourcePosition", [distance_id, x_pos, y_pos, z_pos])
        if is_test:
            with slab.key() as key:
                response = key.getch()
            seq.add_response(response - 48)
        else:
            time.sleep(3)
    file.write(seq, "seq")


test_trials = slab.Trialsequence(conditions=test_conditions, n_reps=5)
run_trials(test_trials, is_test=True)

# training_trials_away = slab.Trialsequence(trials=distance_ids)
# run_trials(training_trials_away)
#
# training_trials_toward = slab.Trialsequence(trials=distance_ids_rev)
# run_trials(training_trials_toward)
#
# training_trials_random = slab.Trialsequence(conditions=distance_ids, n_reps=3)
# run_trials(training_trials_random)
