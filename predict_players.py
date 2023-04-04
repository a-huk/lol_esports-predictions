import csv
import tflearn
import tensorflow as tf

from tflearn.data_utils import load_csv
from parse_players import double_in
'''
Defines a neural network model, trains it and then predicts it.
I could train it once and save/use it afterwards. With the low computation 
and epochs needed to train the model, we train it each time. Hard to find the 
best parameters of the model, these seem to be margianlly better with limited testing.
matches: list of matches/formated team data that we use to predict
returns the prediction info
'''


def predict_players(player_data):
    print("DEBUG")
    print(player_data)
    #Rest tensorflow or it will create errors
    tf.reset_default_graph()
    # Training/validation data loaded
    data, labels = load_csv('./player_out.csv',
                            categorical_labels=True,
                            has_header=False,
                            n_classes=2,
                            target_column=0)
    # Twenty-two variables per team to take into account
    net = tflearn.input_data(shape=[None, 150])
    # Layers of 22, 12 and 3 neurons, produce good results
    net = tflearn.fully_connected(net, 80)
    net = tflearn.fully_connected(net, 60)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 7)
    net = tflearn.fully_connected(net, 2, activation='softmax')
    net = tflearn.regression(net)
    # Define model
    model = tflearn.DNN(net)
    # Start training
    model.fit(data,
              labels,
              n_epoch=35,
              batch_size=32,
              show_metric=True,
              validation_set=0.35)

    prediction_data = []


    player_data = double_in(player_data)
    for match in player_data:
        left_win = match[0]
        right_win = match[1]
        team1 = match[2]
        team2 = match[3]
        print(" ")
        print("----------PLAYER PREDICTING----------")
        print(match[2] + " vs " + match[3])
        t1l, t1w = model.predict([match[0]])[0]
        t2l, t2w = model.predict([match[1]])[0]

        t1_win = (t1w + t2l) / 2
        t2_win = (t2w + t1l) / 2

        print(match[2] + "'s winrate is " + str(round(t1_win, 3)))
        print(match[3] + "'s winrate is " + str(round(t2_win, 3)))

        if t1_win > t2_win:
            print(match[2] + " will win the match")
        elif t2_win > t1_win:
            print(match[3] + " will win the match")
        else:
            print("Will never happen, but it will be a draw")
        print("appending")
        print([match[2], t1_win, match[3], t2_win])
        prediction_data.append([match[2], t1_win, match[3], t2_win])
    return prediction_data

