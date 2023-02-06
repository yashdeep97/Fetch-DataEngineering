Python script to Read data from an SQS Queue, mask Personal Identifiable information (PII) and storethe data in Postgres database.

#### Steps to run ETL Python Script
- Install Python packages from requirements.txt
- run `$ python3 fetch-test.py --buffer_size <number of messages to process>`
- The results can be viewed in the Postgres DB

#### Decisions made:
- How will you read messages from the queue?
Used the Boto3 AWS SDK to read messages from the AWS SQS.
- What type of data structures should be used?
 Used a list to temporarily store messages from the message queue. The list acts as a buffer, allowing us to batch multiple messages together and write them to the database in a single transaction.
- How will you mask the PII data so that duplicate values can be identified?
Masked the PII information using SHA256 hash mechanism provided by the Hashlib package
- What will be your strategy for connecting and writing to Postgres?
Used the psycopg2 PostgreSQL database adapter to execute insert quiries on the database
-  Where and how will your application run?
Steps to run the python application using commandline are mentioned above.

### Additional Questions:
- How would you deploy this application in production?
I would deploy this application using CI/CD pipelines to AWS Lambda with a regular scheduling.
- What other components would you want to add to make this production ready?
To make the code production ready, we need to add unit tests for each function and component. It also needs integration testing to verify connection to service bus and PostgreSQL database.
- How can this application scale with a growing dataset.
Since AWS Lambda manages the underlying resources, we can scale vertically or horizontally by increasing the number of functions. We also need to be careful about writing simultaneosly to the PostgreSQL database and thus will add transactions.
- How can PII be recovered later on?
SHA 256 hashing is irreversible and hence we cannot recover the ip address and device id.
- What are the assumptions you made?
I assumed that we would not need to recover the PII information later.