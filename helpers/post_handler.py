import json
import random


def prepare(type, data, number):
    metadesc = f"Explore a collection of mind-bending riddles that challenge your problem-solving skills and spark your creativity. Perfect for puzzle enthusiasts!"
    # excerpt = data[0]["riddle"]
    titles = [
        "20 Challenging Riddles to Sharpen Your Mind",
        "20 Riddles That Will Push Your Problem",
        "20 Riddles to Challenge Your Logic and Test Your Wit",
        "20 Thought-Provoking Riddles to Exercise Your Brainpower",
        "Boost Your Brain with These 20 Mind-Twisting Riddles",
        "20 Tough Riddles That Will Leave You Stumped",
        "20 Riddles to Stretch Your Imagination",
        "The Ultimate Riddle Collection: 20 Puzzles to Test Your IQ!",
        "20 Intriguing Riddles for You to Solve",
        "20 Riddles to Test Your Wit – How Many Can You Solve?",
        "Ready for a Challenge? 20 Riddles to Test Your Brainpower",
        "20 Tricky Riddles That Will Stump Even the Sharpest Minds",
        "Can You Solve These 20 Brain-Twisting Riddles? Test Your Skills",
        "20 Mind-Boggling Riddles That Will Have You Thinking Hard",
        "Challenge Your Brain with These 20 Mind-Bending Riddles",
        "20 Riddles That Will Make You Look at the World Differently",
        "20 Puzzles to Test Your IQ – Can You Solve Them All?",
        "The Best 20 Riddles to Challenge Your Thinking and Logic",
        "20 Riddles to Improve Your Critical Thinking Skills",
        "Sharpen Your Mind with These 20 Riddles – Ready for the Test?",
        "20 Tough Riddles That Will Keep You Guessing",
        "Brainpower Challenge: Can You Solve These 20 Riddles?",
        "Think You’ve Got It? Solve These 20 Mind-Challenging Riddles",
        "20 Brain-Teasing Puzzles to Push Your Logical Thinking",
        "20 Riddles for Sharp Minds – Are You Ready for the Challenge?",
        "Test Your Mental Strength with These 20 Challenging Riddles",
        "20 Riddles to Keep Your Mind Active and Engaged",
        "Can You Solve These 20 Intriguing Puzzles? Test Your Brain!",
        "20 Riddles to Stretch Your Mind and Boost Your Problem-Solving Skills",
    ]
    # Prepare the post data
    post_data = {
        "title": titles[number],
        "content": json.dumps(data),  # Ensure data is JSON-encoded
        "status": "publish",
        "type": type,  # Custom post type
        "excerpt": metadesc,
        "meta": {  # Metadata (Yoast SEO and others)
            "_yoast_wpseo_focuskw": "challenging riddles",
            "_yoast_wpseo_metadesc": metadesc,
            "_yoast_wpseo_title": titles[number],
        },
    }
    return post_data
