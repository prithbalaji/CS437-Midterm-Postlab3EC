import numpy as np


learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.2


num_states = 10  
num_actions = 2  


q_table = np.zeros((num_states, num_actions))

#example RSSI
rssi_values = [0.2, 0.3, 0.4, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]

packet_detected = [1, 0, 1, 1, 0, 1, 1, 0, 0, 1]

def choose_action(state):
    if np.random.uniform(0, 1) < exploration_prob:
        
        return np.random.choice(num_actions)
    else:
        
        return np.argmax(q_table[state, :])


def q_learning():
    learned_rssi_values = []
    for episode in range(100):  
        state = 0  
        for t in range(len(rssi_values)):
            action = choose_action(state)
            next_state = t
            reward = rssi_values[next_state]  
            
           
            if packet_detected[next_state] == 1:
                reward += 10  
            
            q_table[next_state, action] = (1 - learning_rate) * q_table[state, action] + learning_rate * (reward + discount_factor * np.max(q_table[next_state, :]))
            learned_rssi_values.append(q_table[next_state,0])

            state = next_state
    print(learned_rssi_values)


q_learning()


print("Learned Q-table:")
print(q_table)
print("-------")



