"""
Supabase 连接诊断工具
用于检查和验证 Supabase 数据库连接
"""
import os
import sys
import socket
from urllib.parse import urlparse

def check_env_file():
    """检查 .env 文件"""
    print("=" * 60)
    print("1. 检查 .env 文件")
    print("=" * 60)
    
    if not os.path.exists('.env'):
        print("❌ .env 文件不存在")
        return None
    
    print("✅ .env 文件存在")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL 未设置")
        return None
    
    print("✅ DATABASE_URL 已设置")
    return database_url

def parse_database_url(url):
    """解析数据库 URL"""
    print("\n" + "=" * 60)
    print("2. 解析数据库连接字符串")
    print("=" * 60)
    
    try:
        parsed = urlparse(url)
        
        print(f"协议: {parsed.scheme}")
        print(f"主机: {parsed.hostname}")
        print(f"端口: {parsed.port}")
        print(f"数据库: {parsed.path[1:]}")
        print(f"用户名: {parsed.username}")
        print(f"密码: {'*' * len(parsed.password) if parsed.password else 'None'}")
        
        return {
            'scheme': parsed.scheme,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path[1:],
            'username': parsed.username,
            'password': parsed.password
        }
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return None

def test_dns_resolution(hostname):
    """测试 DNS 解析"""
    print("\n" + "=" * 60)
    print("3. 测试 DNS 解析")
    print("=" * 60)
    
    print(f"尝试解析主机名: {hostname}")
    
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS 解析成功")
        print(f"   IP 地址: {ip_address}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS 解析失败: {e}")
        print("\n可能的原因：")
        print("  1. Supabase 项目还未完全初始化（需要等待 2-3 分钟）")
        print("  2. 主机名不正确（请检查 Supabase 仪表板）")
        print("  3. 网络连接问题")
        return False

def test_port_connection(hostname, port):
    """测试端口连接"""
    print("\n" + "=" * 60)
    print("4. 测试端口连接")
    print("=" * 60)
    
    print(f"尝试连接 {hostname}:{port}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"✅ 端口 {port} 可访问")
            return True
        else:
            print(f"❌ 端口 {port} 不可访问")
            return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_database_connection(url):
    """测试数据库连接"""
    print("\n" + "=" * 60)
    print("5. 测试数据库连接")
    print("=" * 60)
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        
        print("尝试连接到数据库...")
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            connect_timeout=10
        )
        
        print("✅ 数据库连接成功")
        
        # 测试查询
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL 版本: {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def provide_recommendations(results):
    """提供建议"""
    print("\n" + "=" * 60)
    print("6. 诊断结果和建议")
    print("=" * 60)
    
    if all(results.values()):
        print("🎉 所有检查通过！数据库连接正常。")
        print("\n你可以运行以下命令启动应用：")
        print("  python src/main.py")
    else:
        print("⚠️  发现问题，请按照以下建议操作：\n")
        
        if not results.get('env'):
            print("❌ .env 文件或 DATABASE_URL 问题")
            print("   → 确保 .env 文件存在且包含 DATABASE_URL")
            print("   → 运行: cp .env.example .env\n")
        
        if not results.get('dns'):
            print("❌ DNS 解析失败")
            print("   可能的解决方案：")
            print("   1. 检查 Supabase 项目是否完全初始化")
            print("      → 登录 https://supabase.com")
            print("      → 确认项目状态为 'Active'")
            print("      → 等待 2-3 分钟让项目完全启动")
            print()
            print("   2. 验证连接字符串是否正确")
            print("      → Settings → Database → Connection string (URI)")
            print("      → 复制正确的连接字符串")
            print("      → 确保主机名格式正确（db.xxxxx.supabase.co）")
            print()
            print("   3. 尝试使用 Connection Pooling URL")
            print("      → Settings → Database → Connection Pooling")
            print("      → 使用格式: postgresql://postgres.xxx:password@xxx.pooler.supabase.com:6543/postgres")
            print()
        
        if not results.get('port'):
            print("❌ 端口连接失败")
            print("   → 检查防火墙设置")
            print("   → 确认端口号正确（通常是 5432 或 6543）\n")
        
        if not results.get('database'):
            print("❌ 数据库连接失败")
            print("   → 检查用户名和密码是否正确")
            print("   → 在 Supabase 重置密码: Settings → Database → Reset Password")
            print("   → 更新 .env 文件中的 DATABASE_URL\n")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  SUPABASE 连接诊断工具")
    print("=" * 60)
    
    results = {
        'env': False,
        'parse': False,
        'dns': False,
        'port': False,
        'database': False
    }
    
    # 检查 .env 文件
    database_url = check_env_file()
    if database_url:
        results['env'] = True
        
        # 解析 URL
        parsed = parse_database_url(database_url)
        if parsed:
            results['parse'] = True
            
            # 测试 DNS
            if test_dns_resolution(parsed['hostname']):
                results['dns'] = True
                
                # 测试端口
                if test_port_connection(parsed['hostname'], parsed['port']):
                    results['port'] = True
                    
                    # 测试数据库连接
                    if test_database_connection(database_url):
                        results['database'] = True
    
    # 提供建议
    provide_recommendations(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
