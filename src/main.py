import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
users_df = pd.read_csv("users.csv")
liked_posts_df = pd.read_csv("liked_posts.csv")
posts_df = pd.read_csv("posts.csv")

def preprocess_data(username):
    """
    Prepares data for recommendation by extracting user preferences.
    """
    # Get user details
    user = users_df[users_df["username"] == username]
    if user.empty:
        print(f"User '{username}' not found.")
        return None, None

    user_id = user["id"].iloc[0]
    
    # Get posts liked by the user
    user_liked_posts = liked_posts_df[liked_posts_df["user_id"] == user_id]
    
    # If the user has no liked posts, return empty preferences but valid user_id
    if user_liked_posts.empty:
        print(f"User '{username}' has not liked any posts.")
        return pd.DataFrame(), user_id

    # Merge liked posts with posts data for metadata
    liked_post_ids = user_liked_posts["post_id"].unique()
    user_preferences = posts_df[posts_df["id"].isin(liked_post_ids)]
    
    # Create a combined features column for user_preferences
    user_preferences["combined_features"] = user_preferences["title"].fillna("") + " " + \
                                            user_preferences["post_summary.emotions.overall_sentiment"].fillna("") + " " + \
                                            user_preferences["post_summary.actions.coin_rotation"].fillna("")
    
    return user_preferences, user_id

def recommend_posts(username, top_n=5):
    """
    Recommends posts based on the user's preferences or popular posts as a fallback.
    If the user is not found, no posts are recommended.
    """
    user_preferences, user_id = preprocess_data(username)
    
    # Handle user not found case
    if user_id is None:
        print(f"User '{username}' not found. No recommendations can be made.")
        return

    if user_preferences.empty:
        # Recommend popular posts if the user has no preferences
        print(f"No liked posts found for '{username}'. Recommending popular posts:")
        popular_posts = posts_df.sort_values(
            by=["view_count", "rating_count"], ascending=False
        ).head(top_n)

        for idx, post in popular_posts.iterrows():
            print(f"Post Title: {post['title']}")
            print(f"Views: {post['view_count']}")
            print(f"Ratings: {post['rating_count']}")
            print(f"Link: {post['slug']}")
            print()
        return

    # Create a combined features column for all posts
    posts_df["combined_features"] = posts_df["title"].fillna("") + " " + \
                                     posts_df["post_summary.emotions.overall_sentiment"].fillna("") + " " + \
                                     posts_df["post_summary.actions.coin_rotation"].fillna("")

    vectorizer = TfidfVectorizer(stop_words="english")
    post_features = vectorizer.fit_transform(posts_df["combined_features"])
    
    # If there are no preferences, stop execution
    if user_preferences["combined_features"].empty:
        print(f"User preferences have no valid features.")
        return

    # Calculate similarity
    user_pref_features = vectorizer.transform(user_preferences["combined_features"])
    similarity_scores = cosine_similarity(user_pref_features, post_features)
    
    # Get top N recommendations
    mean_similarity = similarity_scores.mean(axis=0)
    recommended_indices = mean_similarity.argsort()[-top_n:][::-1]
    recommended_posts = posts_df.iloc[recommended_indices]
    
    # Display recommendations with explanations
    print(f"Recommendations for {username}:")
    for idx, post in recommended_posts.iterrows():
        reason = "similar content or sentiment"  # Modify this based on the actual features used
        print(f"Post Title: {post['title']} (Reason: You liked posts with {reason})")
        print(f"Sentiment: {post['post_summary.emotions.overall_sentiment']}")
        print(f"Coin Rotation Action: {post['post_summary.actions.coin_rotation']}")
        print(f"Link: {post['slug']}")  # Assuming 'slug' is the URL or identifier
        print()

# Example usage
username_input = "maya"
recommend_posts(username_input, top_n=5)