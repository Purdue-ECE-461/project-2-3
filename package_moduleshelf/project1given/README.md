# Team 2 Project 1 - Trustworthy Modules
This is the github repository for team 2. This contains all the necessary code to get the tool working. This project takes Github or NPM repositories and gives them scores based on the following metrics.

 - **Bus Factor**: How strong is the organization when faced with adversity with pushing changes?
 - **Ramp Up**: How long will it take to set up the repository and get developers to use it?
 - **Correctness**: Does the repository work as intended?
 - **Responsiveness**: How well do developers fix the issues that may be present during usage?
 - **Licensing**: Is the package compliant with ACME standards?

## How to use
### Set Environment Variables

    GITHUB_TOKEN= ''
    LOG_FILE= ''
 We need to set these to make sure that  the we can get information from Github and also make sure that we can log the activity of the program so you may refer to it after a run. 

### Run File
In the root directory, there is a run file. In Linux/UNIX, we want to create an executable to make sure that we can run the tool. Use the following commands to do so.

    chmod +x run
 Now we made the executable and can run the suite of commands that have already been prepared.


## Commands

    ./run install
This will need to be done first as it creates a virtual environment with all the necessary Python packages to run all the code

    ./run TEXT FILE HERE
This will run a grader with all the links to Github or NPM repositories in the text file. It will out produce a stdout with the scores of each repository. With the stdout, you will also get a JSON output that you can view easily. If you provide an invalid link in the txt file, you'll find information about which link failed in the LOG_FILE. 

    ./run test
This will run the test suite we used to test our code for correctness and code quality. Running this command will present statistics on our code coverage and the amount of tests that we passed. 
