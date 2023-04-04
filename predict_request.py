import akkio
import os
import time

'''
Uses Akkio's AI with OE's data, is fed the same data as 
the tflearn predictor
Use your own data and key
'''

def predict_akkio(matches):
	prediction_data = []
	print("-------------------AKKIO PREDICTION-------------------")
	for match in matches:
		print(match[2] + " vs " + match[3])
		left_win = match[0]
		right_win = match[1]
		team1 = match[2]
		team2 = match[3]
		i = 0
		while True:
			try:
				akkio.api_key = "AKKIO_API_KEY"
				prediction = akkio.make_prediction("BssJz3Rf3scL5VFNaiiO", [{"kills_per_game": left_win[0], " deaths_per_game": left_win[1], " game_length": left_win[2], " ckpm": left_win[3], " gpr": left_win[4], " gspd": left_win[5], " gd15": left_win[6], " firstblood": left_win[7], " firsttower": left_win[8], " first3towers": left_win[9], " turret_plates_per_game": left_win[10], " harold_control_rate": left_win[11], " firstdragon": left_win[12], " dragon_control_rate": left_win[13], " elder_control_rate": left_win[14], " baron_control_rate": left_win[15], " firstbaron": left_win[16], " cs_share": left_win[17], " jng_share": left_win[18], " wards_per_minute": left_win[19], " control_wards_purchased_per_minute": left_win[20], " wards_cleared_per_minute": left_win[21], "kills_per_game.1": left_win[22], " deaths_per_game.1": left_win[23], " game_length.1": left_win[24], " ckpm.1": left_win[25], " gpr.1": left_win[26], " gspd.1": left_win[27], " gd15.1": left_win[28], " firstblood.1": left_win[29], " firsttower.1": left_win[30], " first3towers.1": left_win[31], " turret_plates_per_game.1": left_win[32], " harold_control_rate.1": left_win[33], " firstdragon.1": left_win[34], " dragon_control_rate.1": left_win[35], " elder_control_rate.1": left_win[36], " baron_control_rate.1": left_win[37], " firstbaron.1": left_win[38], " cs_share.1": left_win[39], " jng_share.1": left_win[40], " wards_per_minute.1": left_win[41], " control_wards_purchased_per_minute.1": left_win[42], " wards_cleared_per_minute.1" : left_win[43]}], explain=True)
				time.sleep(2)
				prediction2 = akkio.make_prediction("BssJz3Rf3scL5VFNaiiO", [{"kills_per_game": right_win[0], " deaths_per_game": right_win[1], " game_length": right_win[2], " ckpm": right_win[3], " gpr": right_win[4], " gspd": right_win[5], " gd15": right_win[6], " firstblood": right_win[7], " firsttower": right_win[8], " first3towers": right_win[9], " turret_plates_per_game": right_win[10], " harold_control_rate": right_win[11], " firstdragon": right_win[12], " dragon_control_rate": right_win[13], " elder_control_rate": right_win[14], " baron_control_rate": right_win[15], " firstbaron": right_win[16], " cs_share": right_win[17], " jng_share": right_win[18], " wards_per_minute": right_win[19], " control_wards_purchased_per_minute": right_win[20], " wards_cleared_per_minute": right_win[21], "kills_per_game.1": right_win[22], " deaths_per_game.1": right_win[23], " game_length.1": right_win[24], " ckpm.1": right_win[25], " gpr.1": right_win[26], " gspd.1": right_win[27], " gd15.1": right_win[28], " firstblood.1": right_win[29], " firsttower.1": right_win[30], " first3towers.1": right_win[31], " turret_plates_per_game.1": right_win[32], " harold_control_rate.1": right_win[33], " firstdragon.1": right_win[34], " dragon_control_rate.1": right_win[35], " elder_control_rate.1": right_win[36], " baron_control_rate.1": right_win[37], " firstbaron.1": right_win[38], " cs_share.1": right_win[39], " jng_share.1": right_win[40], " wards_per_minute.1": right_win[41], " control_wards_purchased_per_minute.1": right_win[42], " wards_cleared_per_minute.1" : right_win[43]}], explain=True)


				t1w = float(prediction["predictions"][0]['Probability left_win is 1'])
				t1l = float(prediction["predictions"][0]['Probability left_win is 0'])
				t2w = float(prediction2["predictions"][0]['Probability left_win is 1'])
				t2l = float(prediction2["predictions"][0]['Probability left_win is 0'])
			except :
				i = i + 1
				print("Failed: " + str(i))
				continue
			break
			

		t1_win = (t1w + t2l)/2
		t2_win = (t1l + t2w)/2

		print(match[2]+"'s winrate is " + str(round(t1_win,3)))
		print(match[3]+"'s winrate is " + str(round(t2_win,3)))
		
		if t1_win > t2_win:
			print(match[2] + " will win the match")
		elif t2_win > t1_win:
			print(match[3] + " will win the match")
		else:
			print("Will never happen, but it will be a draw")
		prediction_data.append([match[2], t1_win, match[3], t2_win])

	return prediction_data