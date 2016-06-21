
## In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?
I tried several times and found the no matter what state of traffic, lights and position, the primary agent will never move at all. It can never reach the target position.
Other 3 dummy agents have been randomly moving towards random directions.

The basic behaviour those three dummy agents are following the right-of-way rules.
>When the traffic light is green, the agent can take actions follow the random move actions like forward, right and left (if there is no oncoming traffic that coming forward)
>
>When the traffic light is red, the agent will wait and take no action if its next move is forward or Left, but can turn right to the corner if there is no oncoming traffic turning left.

The agents are given unlimited steps reach the destination. Those three agents can eventually reach the target location but in a pure random manner.

## Justify why you picked these set of states, and how they model the agent and its environment.

I choose states as next waypoint, light, status of oncoming agents and status of the left side traffic as four inputs

**Waypoint**: The next waypoint is the directions from the planner is the agent can use the information to reach the destination. Based on planner.py, the next_waypoint sensed the direction f the smartcab for it to follow and finally reach the destination. Without it, the smartcab basically has no way to find its direction. And also based on reward scheme, the smart cap can gets a reward of 2 each time if it follows the waypoint, and a reward of 0.5 if it does not.

**Light** of the signal sets the traffic rules for smartcab to follow. The reward scheme also sets that the smartcab gets penalty if it breaches the rule.

**Oncoming and the left** can be optional status. It states out the traffic situation for the smartcab to follow based on US right-of-way rules

**Right** rule is ignored in this case given its definition is the same with the rule set by the traffic light.

## What changes do you notice in the agent’s behavior?

Qlearning has given the agent more information to learnso that it can learn from the traffic lights and surrounding utility Q values so that I can be easier for it to reach the destination before the deadline.

After several trials, the smartcab can follow the rules set in the states and know what it should act to earn higher rewards. Initially I set alpha as 0.5, gamma as 0.9, epsilon = 1, and number of trials as 100.  The result shows that the smartcab can reach the destination for 33 times in total number of 100 trials, representing a success rate of 33%. Among total number of 2455 steps it experienced in its 100 trials, the smartcab had recorded 17 negative rewards (penalties), accounting for 0.69% of total.

## Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?
**Discount Factor: gamma**
The discount factor gamma determines the importance of future rewards. I initially set gamma as 0.9. however it result in a lower success rate, meaning that the algorithm does not converages as quickly as we expected. I can decrease the gamma so that the smartcab agent gets more penalised when it takes more time to reach the destination (short-sighted). A lower gamma is required to acclerate the algorithm and yield a higher success rate, 98%-99% (shown in the table below).

**Learning Rate:alpha**
For leanring rate, the learning rate determines to what extent the newly acquired information will override the old information. A lower learning rate will make the agent not learn less, while a factor of 1 would make the agent consider only the most recent information. In fully deterministic environments, a learning rate of 1 is optimal. When the problem is stochastic, the algorithm still converges under some technical conditions on the learning rate, that require it to decrease to zero. The basic conditions are that the sum of the learning rates goes to infinity (so that any value could be reached) and that the sum of the squares of the learning rates is finite (which is required to show that the convergence is with probability one). In this case, a lower leanrning rate like 0.1 (table below) results in a lower success rate given the agent is not leanring quickly enough. Thus, we adopt 0.9 constant learning rate in the experiment below. 

**Epsilon**
Initially we set epsilon as fixed number 1, however, given the exploration diminishes over time, and the policy used asymptotically becomes greedy and optimal. It should be better to set epsilon as 1/k  (k = number of trials) as number of trial grows. Thus, I tried a new set of parameters: alpha at 0.9, gamma at 0.4, epsilon =1/k, and number of trials as 100. The change results in a much higher success rate  - 98% and the negative penalised rate at about 1.7% among 1403 moves (note that the number of moves also gets less compared to the previous experiment). These two adjustment should result in the algorithm to find its optimal policy more efficient than before.

| Alpha  | Gamma  | epsilon  | Success Rate  |  Explored moves |  Penalised moves  | Penalised rate  |
|:-:|:-:|:-:|:-:|:-:| :-:| :-:|
|  0.5  | 0.9  |  1 | 33%  | 2455  | 17  | 0.69% |
|  0.5 |  0.4 | 1  |  98% |  1218 |  14 | 1.15% |
|  0.5 | 0.1  | 1  | 98%  | 1403  | 18 | 1.28% |
|    |   |    |  |    |  |  |
|  0.1 | 0.4  | 1  | 87%  | 1554  | 77 | 4.95% |
|  0.5 | 0.4  | 1  |93%  | 1494  | 38 | 2.54% |
|  0.9 | 0.4  | 1  |96%  | 1397  | 30 | 2.15% |
|    |   |    |  |    |  |  |
|  0.9 | 0.4  | 1  |96%  | 1340 | 26 | 1.94% |
|  0.9 | 0.4  | 1/k  |99%  | 1445  | 12 | 0.83% |



**Initial Q value**
Initially I set Q initial condition at 0. However, in about 100 trials, the algorithm converges poorly and only recorded less than 20 succeeded trials to the destination.
Initial action values can also be used as a simple way of encouraging exploration, a higher or a more optimistic initial value should encourage the algorithm explore all actions quickly as in a first few trials. This is because every action the agent explored initially should has a lower Q value compared to the initial Q value.
I tried a few large number such as 5, it converages quickly and achieved higher success rate compared to 0 initial condition.


## Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?
**Performance of the Agent**
*Penalties*
Among 24 moves that reported negative rewards, the penalised moves are mainly occurred in the first few random steps it made. By looking at the detailed move of each penalised actions, those negative-reward moves are mainly involved in breaking traffic rules, for example, when light is red, it goes forward, or left. Some other penalities are incurred when there are oncoming cars and the agent doesn't know what to do at first. The negative moves continue to decrease as number of trials increases.

*Rewards*
The structure of the reward of each trial is normalised for each action move. As each correct action is awarded, without a deadline, the agent tends to go like circles to accumulate poisitive wards with longer distance to the destination. However, once a deadline is set, the agent tends to break the traffic rule (and report much more negative-reward moves) so as to reach the destination. In reality, the reward can be a function of actions and states, or maybe set as *delayed rewards" taking into account the time of its travel or total number of actions it accumulated.

**Conclusion**
In all, after adjusting the gamma, epsilon and the initial Q-value, the algorithm gets more robust in finding an optimal policy. It only takes the first 1st or 2nd trials to learn and can reach the destination from its 3nd trials within 100 trials. The agent is able to get the target destination on time with low chances of incurring accidents or breaking the rules.
