import boto3 # AWS SDK for Python to interact with AWS services
import botocore.config
import json

from datetime import datetime

# Function to generate a blog using Bedrock foundation model
def blog_generate_using_bedrock(blogtopic:str) -> str:
    # Define the prompt to instruct the model to generate a blog
    prompt = f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """

    # Define request body for invoking the Bedrock model
    body = {
        "prompt": prompt,            # Input prompt with the blog topic
        "max_gen_len": 512,          # Maximum length of generated text
        "temperature": 0.5,          # Controls randomness of the output
        "top_p": 0.9                 # Probability distribution for text generation
    }

    try:
        # Initialize Bedrock client to invoke the model (meta.llama3-8b-instruct-v1:0)
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        
        # Invoke the model with the defined body and model ID
        response = bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama3-8b-instruct-v1:0")

        # Read the response content from the Bedrock API
        response_content = response.get('body').read()

        # Convert the JSON response into Python dict
        response_data = json.loads(response_content)

        # Extract the generated blog text from the response
        print(response_data)
        blog_details = response_data['generation'] # Key where generated text is stored
        return blog_details

    except Exception as e:
        # Handle any exceptions that occur during API call
        print(f"Error generating the blog: {e}")
        return ""

# Function to save generated blog to an S3 bucket
def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    # Initialize S3 client to interact with the S3 bucket
    s3 = boto3.client('s3')

    try:
        # Upload the generated blog as a text file to the specified S3 bucket and key
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Blog saved to S3")

    except Exception as e:
        # Handle any exceptions that occur during S3 upload
        print(f"Error when saving the blog to S3: {e}")

# Lambda handler function that orchestrates the blog generation and storage
def lambda_handler(event, context):
    # Extract blog topic from the event's body (JSON format)
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    # Call the function to generate a blog using Bedrock
    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog:
        # Generate a unique S3 key with the current time to avoid overwriting files
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"  # Path and file name for the blog
        s3_bucket = "adhyatma.bucket"              # S3 bucket where the blog will be saved
        
        # Save the generated blog to the S3 bucket
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)

    else:
        # Handle case where no blog is generated
        print("No blog was generated")

    # Return successful response after blog generation and storage
    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed')
    }
