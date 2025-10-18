"""
快速测试 Supabase 连接的脚本
测试多种连接方式
"""
import socket

# 你的密码
PASSWORD = "Xxw981126!"
PROJECT_ID = "nnsimjodhlleqxssaigd"

# 可能的连接字符串格式
connection_strings = {
    "Direct Connection": f"postgresql://postgres:{PASSWORD}@db.{PROJECT_ID}.supabase.co:5432/postgres",
    "Connection Pooling (IPv4)": f"postgresql://postgres.{PROJECT_ID}:{PASSWORD}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres",
    "Connection Pooling (IPv6)": f"postgresql://postgres.{PROJECT_ID}:{PASSWORD}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres",
}

print("=" * 70)
print("  测试 Supabase 连接主机名")
print("=" * 70)

for name, url in connection_strings.items():
    print(f"\n测试 {name}:")
    print("-" * 70)
    
    # 解析主机名
    if "pooler" in url:
        hostname = f"aws-0-ap-southeast-1.pooler.supabase.com"
    else:
        hostname = f"db.{PROJECT_ID}.supabase.co"
    
    print(f"主机名: {hostname}")
    
    # 测试 DNS 解析
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS 解析成功: {ip}")
        print(f"✅ 推荐使用这个连接字符串:")
        print(f"   {url}")
    except socket.gaierror as e:
        print(f"❌ DNS 解析失败: {e}")

print("\n" + "=" * 70)
print("  结论")
print("=" * 70)
print("\n请按照以下步骤操作：")
print("\n1. 到 Supabase 仪表板确认项目状态")
print("   → https://supabase.com")
print("   → 确认项目 'nnsimjodhlleqxssaigd' 存在且状态为 Active")
print("\n2. 获取 Connection Pooling URL（推荐）")
print("   → Settings → Database → Connection Pooling")
print("   → 复制完整的连接字符串")
print("   → 将 [YOUR-PASSWORD] 替换为: Xxw981126!")
print("\n3. 更新 .env 文件中的 DATABASE_URL")
print("\n4. 运行: python diagnose_connection.py")
print("\n5. 如果成功，运行: python src/main.py")
