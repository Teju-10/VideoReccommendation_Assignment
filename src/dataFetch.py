import requests
import pandas as pd

BASE_URL = "https://api.socialverseapp.com"
HEADERS = {
    "Flic-Token": "flic_f42bf01b4d011ceaf602290e39116146a1ed7bbfe73bc949e6b19561a34cf4b8"
}

def fetch_data(endpoint):
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def flatten_users_column(df, column_name):
    """
    Flattens the 'users' column to extract specific fields into their own columns.
    """
    if column_name in df.columns:
        print(f"Checking data in '{column_name}' column:")
        print(df[column_name].head())  # Display the first few rows
        
        if df[column_name].iloc[0] != []:  # Check if it's not an empty list
            users_flat = pd.json_normalize(df[column_name].explode())  # Explode list items if present
            print("Columns after flattening:", users_flat.columns)

            required_fields = [
                "id", "first_name", "last_name", "username", "email", "role", "profile_url", 
                "bio", "website_url", "instagram-url", "youtube_url", "tictok_url", "isVerified", 
                "referral_code", "has_wallet", "last_login", "share_count", "post_count", 
                "following_count", "follower_count", "is_verified", "is_online", "latitude", "longitude"
            ]
            
            missing_fields = [field for field in required_fields if field not in users_flat.columns]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}")

            users_flat = users_flat[users_flat.columns.intersection(required_fields)]
            print(f"Flattened data shape: {users_flat.shape}")
            df = users_flat
        else:
            print("No data found in the 'users' column.")
    return df

def flatten_posts_column(df, column_name):
    """
    Flattens the 'posts' column to extract specific fields into their own columns.
    """
    if column_name in df.columns:
        print(f"Checking the structure of the '{column_name}' column:")
        
        # If the column contains a list of dictionaries
        if isinstance(df[column_name].iloc[0], list):
            # Exploding the list so each dictionary is in its own row
            posts_flat = pd.json_normalize(df[column_name].explode())
            print("Columns after flattening:", posts_flat.columns)  # Print columns after flattening
            
            required_fields = ["id", "post_id", "user_id", "viewed_at"]
            missing_fields = [field for field in required_fields if field not in posts_flat.columns]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}")
            
            posts_flat = posts_flat[required_fields]
            df = posts_flat
        else:
            print(f"Expected a list of dictionaries in column '{column_name}', but found something else.")
    return df
def flatten_liked_posts_column(df, column_name):
    if column_name in df.columns:
        print(f"Inspecting the '{column_name}' column:")
        # Check if 'posts' key exists within the data
        if isinstance(df[column_name].iloc[0], list) and len(df[column_name].iloc[0]) > 0:
            liked_posts_flat = pd.json_normalize(df[column_name].explode())  # Explode the list
            print("Flattened 'liked_posts' columns:", liked_posts_flat.columns)
            
            # Define required fields
            required_fields = ["id", "post_id", "user_id", "liked_at"]
            missing_fields = [field for field in required_fields if field not in liked_posts_flat.columns]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}")
            
            # Keep only required columns and fill missing values
            liked_posts_flat = liked_posts_flat[liked_posts_flat.columns.intersection(required_fields)]
            liked_posts_flat = liked_posts_flat.fillna("No Data")
            
            return liked_posts_flat  # Return the flattened DataFrame
        else:
            print(f"Column '{column_name}' does not contain valid data.")
    return pd.DataFrame()  # Return empty DataFrame if the column is missing or invalid


def flatten_user_ratings_column(df, column_name):
    """
    Flattens the 'user_ratings' column to extract specific fields into their own columns.
    """
    if column_name in df.columns:
        print(f"Inspecting the '{column_name}' column:")
        
        # Check if it's a list with dictionaries inside
        if isinstance(df[column_name].iloc[0], list) and len(df[column_name].iloc[0]) > 0:
            user_ratings_flat = pd.json_normalize(df[column_name].explode())  # Explode the list
            print("Flattened 'user_ratings' columns:", user_ratings_flat.columns)
            
            # Define required fields
            required_fields = ["id", "post_id", "user_id", "rating_percent", "rated_at"]
            missing_fields = [field for field in required_fields if field not in user_ratings_flat.columns]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}")
            
            # Keep only required columns and fill missing values
            user_ratings_flat = user_ratings_flat[user_ratings_flat.columns.intersection(required_fields)]
            user_ratings_flat = user_ratings_flat.fillna("No Data")
            
            return user_ratings_flat  # Return the flattened DataFrame
        else:
            print(f"Column '{column_name}' does not contain valid data.")
    return pd.DataFrame()  # Return empty DataFrame if the column is missing or invalid


def flatten_posts_summary_column(df, column_name):
    """
    Flattens the 'posts' column to extract specific fields into their own columns.
    """
    if column_name in df.columns:
        print(f"Checking the structure of the '{column_name}' column:")
        
        # If the column contains a list of dictionaries
        if isinstance(df[column_name].iloc[0], list):
            # Exploding the list so each dictionary is in its own row
            posts_summary_flat = pd.json_normalize(df[column_name].explode())
            print("Columns after flattening:", posts_summary_flat.columns)  # Print columns after flattening
            
            # Inspecting the first few rows of the flattened data to find the correct fields
            print("First few rows of flattened data:")
            print(posts_summary_flat.head())
            
            # Adjusting required fields based on the actual structure of the flattened data
            required_fields = [
                "id", "slug", "title", "identifier", "comment_count", "upvote_count", "view_count", 
                "rating_count", "average_rating", "post_summary.emotions.overall_sentiment", 
                "post_summary.actions.coin_rotation", "post_summary.audio_elements.auditory_transcription",
                "post_summary.psycological_view_of_video.trait_one",
                "post_summary.psycological_view_of_video.trait_two",
                "post_summary.psycological_view_of_video.trait_three"
                # Add more fields based on what you find in the columns after flattening
            ]
            
            # Check for missing fields
            missing_fields = [field for field in required_fields if field not in posts_summary_flat.columns]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}")
            
            # Only keep the required columns
            posts_summary_flat = posts_summary_flat[posts_summary_flat.columns.intersection(required_fields)]
            
            # Handling missing data (NaN)
            posts_summary_flat = posts_summary_flat.fillna('No Data')  # Replace NaN with 'No Data' or another placeholder
            
            df = posts_summary_flat
        else:
            print(f"Expected a list of dictionaries in column '{column_name}', but found something else.")
    return df


# Endpoints
endpoints = {
    "viewed_posts": "/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "liked_posts": "/posts/like?page=1&page_size=5&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "user_ratings": "/posts/rating?page=1&page_size=5&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "posts": "/posts/summary/get?page=1&page_size=1000",
    "users": "/users/get_all?page=1&page_size=1000"
}

# Revised processing loop
for name, endpoint in endpoints.items():
    data = fetch_data(endpoint)
    df = pd.json_normalize(data)
    
    if name == "viewed_posts":
        # Process and save viewed_posts data
        df = flatten_posts_column(df, "posts")
        df.to_csv(f"{name}.csv", index=False)
        print(f"Processed 'viewed_posts': {df.head()}")
    
    elif name == "liked_posts":
        # Process and save liked_posts data
        print(f"Raw data for {name}: {data}")  # Inspect raw data
        if 'posts' in data:
            liked_posts = data['posts']
            # Convert the 'liked_posts' data into a structured format
            df = pd.DataFrame(liked_posts)
            df['liked_at'] = pd.to_datetime(df['liked_at'])  # Ensure 'liked_at' is a datetime field
            df.to_csv(f"{name}.csv", index=False)
            print(f"Processed 'liked_posts': {df.head()}")
        else:
            print(f"No valid data for {name}.csv")
    
    elif name == "user_ratings":
        # Process and save user_ratings data
        print(f"Raw data for {name}: {data}")  # Inspect raw data
        if 'posts' in data:
            ratings = data['posts']
            # Convert the 'user_ratings' data into a structured format
            df = pd.DataFrame(ratings)
            df['rated_at'] = pd.to_datetime(df['rated_at'])  # Ensure 'rated_at' is a datetime field
            df.to_csv(f"{name}.csv", index=False)
            print(f"Processed 'user_ratings': {df.head()}")
        else:
            print(f"No valid data for {name}.csv")
    
    elif name == "posts":
        # Process and save posts data
        df = flatten_posts_summary_column(df, "posts")
        df.to_csv(f"{name}.csv", index=False)
        print(f"Processed 'posts': {df.head()}")
    
    elif name == "users":
        # Process and save users data
        df = flatten_users_column(df, "users")
        df.to_csv(f"{name}.csv", index=False)
        print(f"Processed 'users': {df.head()}")

print("Data fetching and preprocessing completed. CSV files saved.")
