import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import math

ACTIONS = [None, 'forward', 'left', 'right']

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.counter = 1
        self.steps = 0
        self.acc_steps = 0

        self.alpha = 0.5
        self.gamma = 0.4
        #self.epsilon = 1
        self.epsilon = 1/self.counter

        self.state = None
        self.Q_value = 5
        self.Q = {}

        self.neg_reward_count =0
        self.reward_prev = None
        self.action_prev = None
        self.state_prev = None



    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.steps = 0


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (("directions",self.next_waypoint),
                        ("light",inputs['light']),
                        ("oncoming", inputs['oncoming']),
                        ("left",inputs['left']))
        # TODO: Select action according to your policy

        # move
        Q= self.Q
        if Q.has_key(self.state):
            if random.random() < self.epsilon:
                best_actions = {action: Qhat for action, Qhat in Q[self.state].items() if Qhat == max(Q[self.state].values())}
                action = random.choice(best_actions.keys())
            else:
                action = random.choice (ACTIONS)
        else:
            Q.update({self.state : {act : self.Q_value for act in ACTIONS}})
            action = random.choice (ACTIONS)

        # Execute action and get reward
        reward = self.env.act(self, action)
        if reward < 0:
            self.neg_reward_count += 1

        # TODO: Learn policy based on state, action, reward
        if self.steps:
            Q_hat = (1-self.alpha)*Q[self.state_prev][self.action_prev] + self.alpha * (self.reward_prev + (self.gamma * (max(Q[self.state].values()))))
            Q[self.state_prev][self.action_prev] = Q_hat
            #self.Q = Q

        self.state_prev = self.state
        self.action_prev = action
        self.reward_prev = reward
        self.steps += 1
        self.acc_steps += 1
        self.counter +=1
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track
    # Now simulate it

    sim = Simulator(e, update_delay=0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit

    print "\n\nSuccess rate = {}".format(float(e.des)/100)
    print "Penalty moves = {}".format(a.neg_reward_count)
    print "Total moves = {}".format(a.acc_steps)
    print "Negative Rate = {}".format(float(a.neg_reward_count)/a.acc_steps)
    print "\n\n"
    print a.Q

if __name__ == '__main__':
    run()
