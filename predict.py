import csv
import tflearn

from tflearn.data_utils import load_csv
'''
Defines a neural network model, trains it and then predicts it.
I could train it once and save/use it afterwards. With the low computation 
and epochs needed to train the model, we train it each time. Hard to find the 
best parameters of the model, these seem to be margianlly better with limited testing.
matches: list of matches/formated team data that we use to predict
returns the prediction info
'''


def predict(matches):
    # Training/validation data loaded
    data, labels = load_csv('all_out.csv',
                            categorical_labels=True,
                            n_classes=2,
                            target_column=0)
    # Twenty-two variables per team to take into account
    net = tflearn.input_data(shape=[None, 44])
    # Layers of 22, 12 and 3 neurons, produce good results
    net = tflearn.fully_connected(net, 22)
    net = tflearn.fully_connected(net, 12)
    net = tflearn.fully_connected(net, 3)
    net = tflearn.fully_connected(net, 2, activation='softmax')
    net = tflearn.regression(net)
    # Define model
    model = tflearn.DNN(net)
    # Start training
    model.fit(data,
              labels,
              n_epoch=24,
              batch_size=32,
              show_metric=True,
              validation_set=0.35)

    prediction_data = []

    for match in matches:
        left_win = match[0]
        right_win = match[1]
        team1 = match[2]
        team2 = match[3]
        print(" ")
        print("----------PREDICTING----------")
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
        prediction_data.append([match[2], t1_win, match[3], t2_win])
    return prediction_data
