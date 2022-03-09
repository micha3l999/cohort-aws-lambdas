LAMBDA_NAME="delete_student_PUT"

# Zipping lambda
zip "${LAMBDA_NAME}.zip" lambda_function.py

# Installing python libraries on a ./package folder
pip install --target ./package -r ./requirements.txt
cd package
zip -r "../${LAMBDA_NAME}.zip" .

# Returning to lambda lvl
cd ..

# If you want to create a function, use this command > `create-function` instead `update-function-code`
# And remember use your AWS profile name instead `me`
# Updating function on AWS
aws lambda update-function-code --function-name ${LAMBDA_NAME} --zip-file "fileb://${LAMBDA_NAME}.zip"