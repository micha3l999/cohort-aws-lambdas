# AWS - Cohort Lambdas 

This project was created to handle all lambdas related with Cohort Student project in AWS.

Each lambda is stored under its respectively folder.

### Before to run it
If you do not have any of these lambdas created in your AWS account with the same name, remember 
replace those names in the `./bash` file or, use the command `create-function` instead `update-function-code` 
in the same file. Also, those scripts are using a specific profile called `me`, do not forget replace it with your 
profile name.

### Updating a lambda via terminal
To update a lambda in AWS, run this command at folder level

E.g. updating `students_list_GET` lambda:

- `cd ./students_list_GET`

- `. ./bash.sh`

### References

- If you want to check what are your AWS profiles, check this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

- If you want to learn more about `aws cli` and the commands related with lambda, check this [one](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/lambda/index.html).