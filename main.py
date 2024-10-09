from google.cloud import pubsub_v1, storage
import os, json
from groq import Groq
from api_key import GROQ_API_KEY

# Make Groq Client
groqClient = Groq(
    api_key=GROQ_API_KEY
)

# Add GCP service account key to environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\verit\\OneDrive\\Faizaan Files\\Coding Stuffz\\Python\\Python Projects\\groq-gcp-data-processing\\gcp_service_account_key.json"

def download_blob(bucket_name, file_name):
    # Initialize the client
    client = storage.Client()

    # Reference the bucket and the object (file)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Download the content as text
    file_content = blob.download_as_text()
    print("Got file content. Starting Groq processing...")
    
    # Ask Groq to summarize it
    chat_completion = groqClient.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "I want you to to return a summary of the following text and nothing else: " + file_content[0:7000],
            }
        ],
        model="llama3-8b-8192",
    )

    # Update document with summary
    print("Got Groq response. Updating document...")
    updated_content = chat_completion.choices[0].message.content + "\n--------------------------------------------------------------------\n" + file_content
    metadata = blob.metadata or {}  # Get existing metadata or an empty dictionary
    metadata['summarized'] = 'true'  # Update the summarized field

    # Set the new metadata
    blob.metadata = metadata
    blob.patch()  # Update the metadata in GCS
    blob.upload_from_string(updated_content)
    
    print("Document updated successfully.")


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('direct-abacus-438022-p0', 'documents-sub')

def callback(message):
    print("Received message: ", message.data.decode('utf-8'))
    message_data = message.data.decode('utf-8')
    
    # Get the message data for json messages only
    if message_data[0] == "{":

        # Parse the JSON data
        file_metadata = json.loads(message_data)
        
        if 'metadata' not in file_metadata.keys() or 'summarized' not in file_metadata["metadata"].keys() or file_metadata["metadata"]["summarized"] != "true":
            download_blob('uploaded_documents_bucket', file_metadata["name"])
    message.ack()

# Subscribe to the topic
future = subscriber.subscribe(subscription_path, callback=callback)

# Keep the main thread alive to listen for messages asynchronously
try:
    print("Listening for messages on Pub/Sub...")
    future.result()  # This will block and keep the subscriber running
except KeyboardInterrupt:
    print("Shutting down gracefully...")
    future.cancel()  # Cancel subscription on interrupt
    future.result()  # Wait for the cancellation to complete
