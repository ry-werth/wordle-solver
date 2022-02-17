# wordle-solver
This notebook contains code to help you beat the word game [Wordle](https://www.powerlanguage.co.uk/wordle/)

Read my article on this code [here](https://medium.com/p/298d05b7685/)


https://user-images.githubusercontent.com/29679635/151480622-7bf6d854-376e-4a9a-bbf5-506f14661e44.mp4


### Selenium

Some of the solvers use [Selenium](https://www.selenium.dev/) to interect with the browser. 

You can read the set up and documentation [here](https://pypi.org/project/selenium/).
This code requires a Firefox driver which you can download [here](https://github.com/mozilla/geckodriver/releases).

# Set Up
1. $ `git clone https://github.com/ry-werth/https://github.com/ry-werth/wordle-solver.git`     # Cloning project repository
2. $ `cd wordle-solver`    # Enter to project directory
3. $ `python3 -m venv my_venv`     # If not created, creating virtualenv
4. $ `source ./my_venv/bin/activate`     # Activating virtualenv
5. (my_venv)$ `pip3 install -r ./requirements.txt`     # Installing dependencies
6. (my_venv)$ `deactivate`    # When you want to leave virtual environment

# Solvers
There are 5 Solvers to explore:

1. solver_playground.py
   - This solver allows you to input a guess and target word
   - The solver will print it's guesses as it hones in on the target
   - Run with `python3 solver_playground.py -g [guess word] -t [target word]`

2. solver_assistant.py
   - This solver is used while you play wordle
   - This solver starts with a random word
   - It will ask you to input the result after every guess
   - Run with `python3 solver_assistant.py`

3. solver_popular_letters.py
   - This solver uses Selenium to solve the puzzle on it's own in the browser
   - This solver allows you to input an optional initial guess or it will randomly choose one
   - It uses basic letter popularity to chooses guesses
   - Run with `python3 solver_popular_letters.py -g [guess word]`

4. solver_final.py
   - This solver improves upon solver_popular_letters
   - It uses letter popularity and placement to choose guesses
   - Run with `python3 solver_final.py -g [guess word]`

5. solver_efficency_tester.py
   - This solver is used to test the preformance of the algorithm
   - It loops through every target word attempting to guess it and keep tracks of guesses
   - You can feed it an optional starting guess word
   - Run with `python3 solver_efficency_tester.py -g [guess word]`




