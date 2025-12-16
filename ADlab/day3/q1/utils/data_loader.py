"""
Data Loader for Spam Email Dataset
Loads real spam email data from online sources
"""

import numpy as np
import pandas as pd
import os
from urllib.request import urlretrieve

def load_spam_data(use_real_data=True):
    """
    Load spam email dataset.
    First tries to load real SMS Spam Collection dataset from UCI repository.
    Falls back to synthetic data if download fails.
    
    Args:
        use_real_data: If True, tries to download real dataset
    
    Returns:
        emails: List of email texts
        labels: List of labels (0=non-spam, 1=spam)
    """
    
    if use_real_data:
        try:
            print("    Attempting to download SMS Spam Collection dataset from UCI...")
            return load_sms_spam_dataset()
        except Exception as e:
            print(f"    Failed to download real dataset: {e}")
            print("    Falling back to synthetic data...")
            return generate_synthetic_data()
    else:
        return generate_synthetic_data()

def load_sms_spam_dataset():
    """
    Download and load the SMS Spam Collection dataset from UCI repository.
    
    Returns:
        emails: List of SMS texts
        labels: List of labels (0=ham, 1=spam)
    """
    # URL for SMS Spam Collection dataset
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    
    # Download and read the dataset
    print("    Downloading from GitHub repository...")
    df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])
    
    print(f"    ✓ Successfully loaded {len(df)} real SMS messages!")
    
    # Convert labels to binary (0=ham, 1=spam)
    labels = (df['label'] == 'spam').astype(int).tolist()
    emails = df['message'].tolist()
    
    return emails, labels

def generate_synthetic_data(num_samples=1000):
    """
    Generate synthetic spam and non-spam emails as fallback.
    
    Args:
        num_samples: Total number of emails to generate
    
    Returns:
        emails: List of email texts
        labels: List of labels (0=non-spam, 1=spam)
    """
    
    print(f"    Generating {num_samples} synthetic emails...")
    np.random.seed(42)
    
    # Spam keywords and patterns
    spam_keywords = [
        'free', 'win', 'winner', 'cash', 'prize', 'offer', 'click here',
        'buy now', 'limited time', 'act now', 'congratulations', 'claim',
        'urgent', 'discount', 'cheap', 'deal', 'bonus', 'gift', '$$$',
        'make money', 'work from home', 'earn extra', 'guarantee',
        'no obligation', 'risk free', 'call now', 'order now', 'viagra',
        'pharmacy', 'credit', 'debt', 'loan', 'mortgage', 'refinance'
    ]
    
    # Non-spam (ham) keywords and patterns
    ham_keywords = [
        'meeting', 'schedule', 'report', 'project', 'deadline', 'team',
        'please review', 'attached', 'document', 'presentation', 'update',
        'follow up', 'regarding', 'discussion', 'conference', 'invitation',
        'thank you', 'appreciate', 'best regards', 'sincerely', 'regards',
        'hello', 'hi', 'hope', 'looking forward', 'let me know',
        'feedback', 'question', 'clarification', 'information', 'details'
    ]
    
    emails = []
    labels = []
    
    # Generate spam emails (50%)
    num_spam = num_samples // 2
    for _ in range(num_spam):
        num_words = np.random.randint(10, 30)
        words = np.random.choice(spam_keywords, size=num_words, replace=True)
        
        # Add some generic words
        generic_words = ['the', 'a', 'and', 'to', 'for', 'you', 'your', 'this', 'is']
        generic_count = np.random.randint(5, 15)
        words = np.append(words, np.random.choice(generic_words, size=generic_count, replace=True))
        
        np.random.shuffle(words)
        email_text = ' '.join(words)
        emails.append(email_text)
        labels.append(1)  # Spam
    
    # Generate non-spam emails (50%)
    num_ham = num_samples - num_spam
    for _ in range(num_ham):
        num_words = np.random.randint(15, 35)
        words = np.random.choice(ham_keywords, size=num_words, replace=True)
        
        # Add generic words
        generic_words = ['the', 'a', 'and', 'to', 'for', 'you', 'your', 'this', 'is', 'we', 'our']
        generic_count = np.random.randint(8, 20)
        words = np.append(words, np.random.choice(generic_words, size=generic_count, replace=True))
        
        np.random.shuffle(words)
        email_text = ' '.join(words)
        emails.append(email_text)
        labels.append(0)  # Non-spam
    
    # Shuffle the dataset
    indices = np.arange(len(emails))
    np.random.shuffle(indices)
    emails = [emails[i] for i in indices]
    labels = [labels[i] for i in indices]
    
    print(f"    ✓ Generated {len(emails)} synthetic emails")
    return emails, labels

if __name__ == "__main__":
    # Test the data loader
    print("Testing real data loader...")
    emails, labels = load_spam_data(use_real_data=True)
    print(f"\nLoaded {len(emails)} messages")
    print(f"Spam: {sum(labels)}, Non-spam: {len(labels) - sum(labels)}")
    print(f"\nSample spam message:\n{emails[labels.index(1)]}")
    print(f"\nSample non-spam message:\n{emails[labels.index(0)]}")
