# Snail jumper
**Neuroevolution game assignment.**  
**Fall 2022 - Computer Intelligence.**  

# Snail jumper
**Neuroevolution game assignment.**  
**Fall 2022 - Computer Intelligence.**  

# Evolutionary Algorithm for Training Neural Network in Snail Jumper Game

This repository showcases the development of an evolutionary algorithm designed to train a neural network in the Snail Jumper game environment. The challenge here is to achieve effective performance in situations where there isn't sufficient data for traditional learning approaches.

## Introduction

In the Snail Jumper game environment, the neural network's output serves as a decision-maker, determining whether to initiate a jump by pressing the space button.

## Evolutionary Algorithm Approach

The project employs an evolutionary algorithm to enhance the neural network's performance. Here's how it works:

1. **Initial Population**: Start with an initial population of 300 players, each equipped with a neural network.

2. **Fitness-Based Selection**: Players are evaluated based on their performance in the game. Fitness scores guide the selection of players for the next generation.

3. **Crossover**: Apply proper crossover techniques to combine genetic information from selected players. This process aims to create new individuals with potentially improved traits.

4. **Mutation**: Introduce controlled mutations to the genetic makeup of selected players. Mutation injects diversity and helps explore new strategies.

5. **Generation Iteration**: Repeat the selection, crossover, and mutation steps for multiple generations.

## Results

After several generations of evolution using the described algorithm, the players' performance surpassed the baseline by an impressive 50%. This demonstrates the power of the evolutionary approach in enhancing neural network decision-making strategies even when limited data is available.

### Evolution Progress

**Generation: 2**
![generation 2](generation_2.jpg)
*Generation: 2
BScore: 64
*
![generation 5](generation_5.jpg)
*Generation: 5
BScore: 113
*
![generation 17](generation_17.jpg)
*Generation: 17
BScore: 304
*
## Acknowledgments

We extend our gratitude to the open-source community for providing the tools and frameworks that enabled the development of this project.

## Contributing

Contributions to this repository are appreciated! If you have ideas for improvements or extensions, feel free to fork the repository and submit pull requests.

