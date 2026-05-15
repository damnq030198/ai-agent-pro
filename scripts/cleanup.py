import os
import shutil
import redis
from pathlib import Path

def cleanup():
    print("🧹 Starting System Cleanup...")

    # 1. Xóa các file log
    log_file = Path("data/logs/ai_agent.log")
    if log_file.exists():
        log_file.unlink()
        print(f"🗑️ Deleted log file: {log_file}")

    # 2. Xóa cache tạm trong thư mục (nếu có)
    cache_dir = Path("data/cache")
    for item in cache_dir.iterdir():
        if item.is_file():
            item.unlink()
    print(f"🗑️ Cleared local cache directory: {cache_dir}")

    # 3. Xóa AI Cache trong Redis
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        keys = r.keys("ai_cache:*")
        if keys:
            r.delete(*keys)
            print(f"🗑️ Cleared {len(keys)} AI responses from Redis cache")
    except Exception as e:
        print(f"⚠️ Could not connect to Redis for cleanup: {e}")

    print("\n✅ Cleanup completed!")

if __name__ == "__main__":
    cleanup()
