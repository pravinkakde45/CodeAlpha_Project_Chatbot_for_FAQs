import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# List of FAQs (questions and answers)
faq_data = {
    "What is your product?": "Our product is an AI-powered tool that helps users with language translation and information retrieval.",
    "How do I purchase your product?": "You can purchase our product online via our website.",
    "What are the payment methods?": "We accept credit cards, PayPal, and bank transfers.",
    "Do you offer customer support?": "Yes, we offer 24/7 customer support via chat, email, and phone.",
    "How can I contact customer support?": "You can contact us via our website's chat feature, by emailing support@company.com, or by calling our support line."
}

# Preprocess input by tokenizing, removing punctuation, stop words, and lemmatizing
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords.words('english')]
    return tokens

# Calculate similarity between two sets of tokens
def calculate_similarity(user_tokens, faq_tokens):
    user_synsets = [wordnet.synsets(token) for token in user_tokens]
    faq_synsets = [wordnet.synsets(token) for token in faq_tokens]

    score = 0
    for user_word_synsets in user_synsets:
        for faq_word_synsets in faq_synsets:
            if user_word_synsets and faq_word_synsets:  # Check if synsets exist for the word
                max_similarity = max((user_synset.wup_similarity(faq_synset) or 0) for user_synset in user_word_synsets for faq_synset in faq_word_synsets)
                score += max_similarity
    
    return score

# Respond to user query
def get_response(user_query):
    user_tokens = preprocess(user_query)
    
    max_similarity = 0
    best_match = None
    
    for faq_question, faq_answer in faq_data.items():
        faq_tokens = preprocess(faq_question)
        similarity = calculate_similarity(user_tokens, faq_tokens)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = faq_answer
    
    if max_similarity > 0.2:  # Set a threshold for the similarity score
        return best_match
    else:
        return "I'm sorry, I don't have an answer to that question. Please contact support."

# Chatbot interaction with user input
if __name__ == "__main__":
    print("Hello! I am your FAQ bot. How can I help you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = get_response(user_input)
        print(f"Bot: {response}")
