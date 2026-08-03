"""
Universal Upload Orchestrator - Upload to All Social Media Platforms
Uploads generated Arabic learning videos to all configured platforms
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Import individual upload modules
from upload_to_youtube import upload_to_youtube, get_authenticated_service
from upload_instagram import upload_to_instagram
from upload_facebook import upload_to_facebook, upload_to_facebook_story
from upload_telegram import upload_to_telegram
from upload_threads import upload_to_threads
from upload_tiktok import upload_to_tiktok
from upload_twitter import upload_to_twitter
from upload_vk import upload_to_vk


def generate_video_metadata(category_english, category_arabic, phrases):
    """Generate optimized metadata for social media from content"""

    # Build description with all phrases
    description_lines = [
        f"🇸🇦 Learn Arabic with Velocity Arabic! 🇸🇦",
        f"",
        f"📚 Category: {category_english} ({category_arabic})",
        f"",
        f"🎯 Master Arabic one phrase at a time! Today's {category_english} lesson:",
        f""
    ]

    # Add all phrases with emojis
    if phrases:
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        for i, phrase in enumerate(phrases[:5], 0):
            emoji = emojis[i] if i < len(emojis) else f"{i+1}."
            description_lines.append(f"{emoji} {phrase['english']}")
            description_lines.append(f"   📍 {phrase['arabic']}")
            description_lines.append(f"   🔊 [{phrase.get('pronunciation', '')}]")
            description_lines.append("")

    # Call to action and hashtags
    description_lines.extend([
        f"💡 Tip: Repeat each phrase out loud 3 times!",
        f"👍 Like this video if you learned something new!",
        f"💬 Comment your favorite phrase below!",
        f"🔔 Subscribe for daily Arabic lessons!",
        f"",
        f"📖 Pronunciation Guide:",
        f"   The phonetic spelling in brackets helps you say it correctly!",
        f"",
        f"#LearnArabic #ArabicLessons #ArabicForBeginners #LanguageLearning",
        f"#Arabic #Education #Tutorial #DailyArabic #{category_english.replace(' ', '')}",
        f"#VelocityArabic #ArabicPhrases #SpeakArabic"
    ])

    description = "\n".join(description_lines)

    title = f"Arabic Learning: {len(phrases)} Essential {category_english} Phrases 🇸🇦"

    # Generate tags
    tags = [
        'learn arabic',
        'arabic lessons',
        'arabic for beginners',
        'arabic phrases',
        'language learning',
        'arabic tutorial',
        'speak arabic',
        category_english.lower(),
        'education',
        'daily arabic',
        'velocity arabic',
        'arabic learning'
    ]

    return {
        'title': title,
        'description': description,
        'tags': tags,
        'category': category_english
    }


def upload_to_all_platforms(video_path, metadata, platforms=None):
    """
    Upload video to all configured social media platforms
    
    Args:
        video_path: Path to video file
        metadata: Dict with title, description, tags
        platforms: List of platforms to upload to (None = all available)
    
    Returns:
        dict: Upload results for each platform
    """
    
    results = {
        'youtube': {'status': 'pending'},
        'instagram': {'status': 'pending'},
        'facebook': {'status': 'pending'},
        'facebook_story': {'status': 'pending'},
        'telegram': {'status': 'pending'},
        'tiktok': {'status': 'pending'},
        'twitter': {'status': 'pending'},
        'vk': {'status': 'pending'},
        'threads': {'status': 'pending'}
    }
    
    if platforms is None:
        platforms = list(results.keys())
    
    print("\n" + "=" * 80)
    print("🚀 STARTING MULTI-PLATFORM UPLOAD")
    print("=" * 80)
    print(f"📹 Video: {video_path}")
    print(f"📝 Title: {metadata['title']}")
    print(f"🎯 Platforms: {', '.join(platforms)}")
    print("=" * 80)
    
    # YouTube
    if 'youtube' in platforms:
        try:
            print("\n📺 YOUTUBE UPLOAD...")
            result = upload_to_youtube(
                video_path=video_path,
                title=metadata['title'],
                description=metadata['description'],
                tags=metadata['tags'],
                category_id='27'  # Education
            )
            results['youtube'] = {'status': 'success', 'result': result}
            print("✅ YouTube upload complete!")
        except Exception as e:
            results['youtube'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ YouTube upload failed: {e}")
    
    # Instagram Reels
    if 'instagram' in platforms:
        try:
            print("\n📸 INSTAGRAM REELS UPLOAD...")
            result = upload_to_instagram(
                video_path=video_path,
                caption=metadata['description'][:2200],
                is_story=False
            )
            results['instagram'] = {'status': 'success', 'result': result}
            print("✅ Instagram upload complete!")
        except Exception as e:
            results['instagram'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Instagram upload failed: {e}")
    
    # Facebook Reels
    if 'facebook' in platforms:
        try:
            print("\n📘 FACEBOOK REELS UPLOAD...")
            result = upload_to_facebook(
                video_path=video_path,
                description=metadata['description'],
                title=metadata['title']
            )
            results['facebook'] = {'status': 'success', 'result': result}
            print("✅ Facebook upload complete!")
        except Exception as e:
            results['facebook'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Facebook upload failed: {e}")
        try:
            print("\n📘 FACEBOOK STORY UPLOAD...")
            story_result = upload_to_facebook_story(
                video_path=video_path,
                description=metadata['description'],
                title=metadata['title']
            )
            results['facebook_story'] = {'status': 'success', 'result': story_result}
            print("✅ Facebook Story upload complete!")
        except Exception as e:
            results['facebook_story'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Facebook Story upload failed: {e}")
    
    # Telegram
    if 'telegram' in platforms:
        try:
            print("\n📱 TELEGRAM UPLOAD...")
            result = upload_to_telegram(
                video_path=video_path,
                caption=metadata['description']
            )
            if result.get('status') == 'skipped':
                results['telegram'] = {'status': 'skipped', 'reason': result.get('reason')}
                print("⚠️ Telegram upload skipped (missing credentials)")
            else:
                results['telegram'] = {'status': 'success', 'result': result}
                print("✅ Telegram upload complete!")
        except Exception as e:
            results['telegram'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Telegram upload failed: {e}")
    
    # TikTok
    if 'tiktok' in platforms:
        try:
            print("\n🎵 TIKTOK UPLOAD...")
            result = upload_to_tiktok(
                video_path=video_path,
                description=metadata['description']
            )
            results['tiktok'] = {'status': 'success', 'result': result}
            print("✅ TikTok upload complete!")
        except Exception as e:
            results['tiktok'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ TikTok upload failed: {e}")
    
    # Twitter/X
    if 'twitter' in platforms:
        try:
            print("\n🐦 TWITTER UPLOAD...")
            result = upload_to_twitter(
                video_path=video_path,
                description=metadata['description']
            )
            results['twitter'] = {'status': 'success', 'result': result}
            print("✅ Twitter upload complete!")
        except Exception as e:
            results['twitter'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Twitter upload failed: {e}")
    
    # VK
    if 'vk' in platforms:
        try:
            print("\n🔵 VK UPLOAD...")
            result = upload_to_vk(
                video_path=video_path,
                description=metadata['description']
            )
            results['vk'] = {'status': 'success', 'result': result}
            print("✅ VK upload complete!")
        except Exception as e:
            results['vk'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ VK upload failed: {e}")
    
    # Threads
    if 'threads' in platforms:
        try:
            print("\n🧵 THREADS UPLOAD...")
            result = upload_to_threads(
                video_path=video_path,
                caption=metadata['description'][:500]
            )
            results['threads'] = {'status': 'success', 'result': result}
            print("✅ Threads upload complete!")
        except Exception as e:
            results['threads'] = {'status': 'failed', 'error': str(e)}
            print(f"❌ Threads upload failed: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 UPLOAD SUMMARY")
    print("=" * 80)
    
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    failed_count = sum(1 for r in results.values() if r['status'] == 'failed')
    skipped_count = sum(1 for r in results.values() if r['status'] == 'skipped')
    
    for platform, result in results.items():
        icon = "✅" if result['status'] == 'success' else ("❌" if result['status'] == 'failed' else "⚠️")
        print(f"{icon} {platform.capitalize()}: {result['status'].upper()}")
    
    print(f"\n📈 Total: {success_count} successful, {failed_count} failed, {skipped_count} skipped")
    print("=" * 80)
    
    return results


def main():
    """Main upload function - uploads the latest generated video"""
    
    # Find the generated video
    video_path = Path('output/final_video.mp4')
    
    if not video_path.exists():
        print("❌ No video found at output/final_video.mp4")
        return False
    
    # Load content metadata if available
    content_file = Path('output/content.json')
    metadata = None
    
    if content_file.exists():
        import json
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            category = content.get('category', 'Arabic Learning')
            phrases = content.get('phrases', [])
            
            # Translate category (simple mapping)
            category_map = {
                'التحيات اليومية': 'Daily Greetings',
                'العبارات الشائعة': 'Common Phrases',
                'الطعام والطعام': 'Food & Dining',
                'أساسيات السفر': 'Travel Essentials',
                'الأرقام والوقت': 'Numbers & Time',
                'العائلة والعلاقات': 'Family & Relationships',
                'التسوق': 'Shopping',
                'الاتجاهات': 'Directions',
                'الطقس': 'Weather',
                'العواطف والمشاعر': 'Emotions & Feelings',
                'العمل والأعمال': 'Work & Business',
                'الصحة والجسد': 'Health & Body',
                'الألوان والأوصاف': 'Colors & Descriptions',
                'الحيوانات': 'Animals',
                'الهوايات والأنشطة': 'Hobbies & Activities',
                'الدافع': 'Motivation',
                'الحب': 'Love',
                'النجاح': 'Success',
                'الحكمة': 'Wisdom',
                'السعادة': 'Happiness',
            }
            
            category_english = category_map.get(category, category)
            metadata = generate_video_metadata(category_english, category, phrases)
            
        except Exception as e:
            print(f"⚠️ Could not load content.json: {e}")
    
    # Use default metadata if not available
    if not metadata:
        metadata = generate_video_metadata(
            'Arabic Learning',
            'تعلم العربية',
            [{'english': 'Sample phrase', 'arabic': 'عينة عبارة'}]
        )
    
    # Determine which platforms to upload to
    # Skip platforms without credentials
    platforms_to_upload = []
    
    # Check YouTube
    if os.getenv('YOUTUBE_CLIENT_ID') or os.getenv('YT_CLIENT_ID'):
        platforms_to_upload.append('youtube')
    
    # Check Instagram
    if os.getenv('INSTAGRAM_ACCESS_TOKEN') or os.getenv('FACEBOOK_ACCESS_TOKEN'):
        platforms_to_upload.append('instagram')
    
    # Check Facebook
    if os.getenv('FACEBOOK_ACCESS_TOKEN') or os.getenv('FB_ACCESS_TOKEN'):
        platforms_to_upload.append('facebook')
    
    # Check Telegram
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        platforms_to_upload.append('telegram')
    
    # Check TikTok (placeholder for now)
    platforms_to_upload.append('tiktok')
    
    # Check Twitter
    if os.getenv('TWITTER_API_KEY') or os.getenv('TWITTER_BEARER_TOKEN'):
        platforms_to_upload.append('twitter')
    
    # Check VK
    if os.getenv('VK_ACCESS_TOKEN'):
        platforms_to_upload.append('vk')
    
    # Check Threads
    if os.getenv('THREADS_ACCESS_TOKEN'):
        platforms_to_upload.append('threads')
    
    if not platforms_to_upload:
        print("⚠️ No platforms configured! Set credentials in .env file")
        print("Configured platforms will be auto-detected from environment variables")
        return False
    
    # Upload to all configured platforms
    results = upload_to_all_platforms(
        video_path=str(video_path),
        metadata=metadata,
        platforms=platforms_to_upload
    )
    
    # Return success if at least one platform succeeded
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    return success_count > 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
