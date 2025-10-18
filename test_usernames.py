"""
测试不同的 Supabase 用户名格式
"""
import psycopg2

PASSWORD = "EwmvE3PTsaAP10bD"
HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
PORT = 6543
DATABASE = "postgres"
PROJECT_ID = "nnsimjodhlleqxssaigd"

# 不同的用户名格式
usernames = [
    f"postgres.{PROJECT_ID}",
    "postgres",
    PROJECT_ID,
    f"postgres_{PROJECT_ID}",
]

print("=" * 70)
print("  测试不同的用户名格式")
print("=" * 70)

for username in usernames:
    print(f"\n尝试用户名: {username}")
    print("-" * 70)
    
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=username,
            password=PASSWORD,
            connect_timeout=10
        )
        
        print(f"✅ 连接成功！")
        print(f"✅ 正确的用户名格式是: {username}")
        print(f"\n完整的连接字符串：")
        print(f"postgresql://{username}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        
        # 测试查询
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f"\n✅ PostgreSQL 版本: {version[:60]}...")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 找到正确的格式了！请更新 .env 文件。")
        break
        
    except Exception as e:
        print(f"❌ 连接失败: {str(e)[:100]}")

print("\n" + "=" * 70)
