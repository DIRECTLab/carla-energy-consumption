# Notes on the process for getting Reinforcement Learning working with Carla for the charger pad placement
## Links
* [End-to-end learning using CARLA Simulator](https://imtiazulhassan.medium.com/end-to-end-learning-using-carla-simulator-12869b5d6f7)
    * Will I need to get the ROS bridge working to do reinforcement learning? I know they supposedly made it more integrated or easier or something in carlaUE5 to use the ROS.
* [Video: RL in Carla](https://www.youtube.com/watch?v=y4ZMg1YPkZM)
  * [More Details from the Video](https://www.dsinnovators.com/blogs/implementing-reinforcement-learning-algorithm-in-carlas-environment)
* [Farama Tools for RL training](https://farama.org/)
* `OpenAI gym` is a tool for doing Reinforcement Learning
* [Docs by OpenAI to learn RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)
* [Stanford DeepLearning Tutorial](http://ufldl.stanford.edu/tutorial/)
* [Stanford RL Course](https://www.youtube.com/watch?v=FgzM3zpZ55o&list=PLoROMvodv4rOSOPzutgyCTapiGlY2Nd8u)

### From Videos
* [Python code example for Reinforcement Learning](https://github.com/Duane321/mutual_information/blob/main/videos/monte_carlo_for_RL_and_off_policy_methods/blackjack.py)

## Structure
Possible Actions:
* Different paths the vehicle can take.
* Changing the placement of the pads.


Rewards:
* Negative 
    1. for hitting other vehicles, lane cutting, (bad/dangerous driving)
* Positive
    1. Having the highest charge in the battery upon reaching destination
    2. Greatest time spent charging whilst still staying under the required travel time


## Questions
1. Should we have the driving (paths, steering, etc) AND the placement of the charger pads be variables for the RL, or have charger pad placement be variable whilst the driving of the vehicle is constant.
    * Can we do both at the same time?