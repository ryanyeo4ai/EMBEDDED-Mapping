import pickle

profile_file = open('profile.pkl', 'rb')
profile = pickle.load(profile_file)
user_id = profile['email']
passwd = profile['pass']
profile_file.close()

print(profile)