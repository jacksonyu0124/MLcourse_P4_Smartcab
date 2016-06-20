
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
After several trials, the smartcab can follow the rules set in the states and know what it should act to earn higher rewards. Initially I set alpha as 0.5, gamma as 0.9, epsilon =1, and number of trials as 100.  The result shows that the smartcab can reach the destination for 67 times in total number of 100 trials, representing a success rate of 67%. Among total number of 1879 steps it experienced in its 100 trials, the smartcab had recorded 65 negative rewards (penalties), accounting for 3.4% of total.

## Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?
We initially sets gamma as 0.9. We can decrease the gamma so that the smartcab agent gets more penalised when it takes more time to reach the destination.
Initially we set epsilon as fixed number 1, however, given the exploration diminishes over time, and the policy used asymptotically becomes greedy and optimal. It can be better to set epsilon as 1/k  (k = number of trials) as number of trial grows.

Thus, I tried a new set of parameters: alpha at 0.5, gamma at 0.4, epsilon =1/k, and number of trials as 100. The change results in a much higher success rate  - 98% and the negative penalised rate at about 1.7% among 1403 moves (note that the number of moves also gets less compared to the previous experiment).

## Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?
Yes, after adjusting the gamma and epsilon, the algorithm gets faster to find an optimal policy. It only takes the first 1 or 2 trials to reach the destination within 100 trials. Among all the moves it takes in the 100 trials, the penalised moves are mainly occurred in the first few random steps it made.  As the number of steps grows, the smartcab gets learning from previous experience.
