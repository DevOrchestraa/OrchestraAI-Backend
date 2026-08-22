import asyncio
from sqlalchemy import text 
from app.database.config import settings
from app.database.db import engine, init_db


async def test_database_connection():
    print("Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            print(f"✓ Connection successful! Result: {row}")
            return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


async def test_create_table():
    print("\nTesting table creation...")
    
    try:
        await init_db()
        print("✓ Tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        return False


async def test_insert_and_query():
    print("\nTesting insert and query...")
    
    try:
        async with engine.connect() as conn:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            await conn.commit()
            
            await conn.execute(text("INSERT INTO test_table (name) VALUES (:name)"), {"name": "test_data"})
            await conn.commit()
            
            result = await conn.execute(text("SELECT name FROM test_table WHERE name = :name"), {"name": "test_data"})
            row = result.fetchone()
            
            if row and row[0] == "test_data":
                print(f"✓ Insert and query successful! Retrieved: {row[0]}")
                
                await conn.execute(text("DROP TABLE test_table"))
                await conn.commit()
                return True
            else:
                print("✗ Query returned unexpected result")
                return False
    except Exception as e:
        print(f"✗ Insert/query test failed: {e}")
        return False


async def main():
    print("=" * 60)
    print("OrchestraAI Database Connection Test")
    print("=" * 60)
    
    tests = [
        ("Connection", test_database_connection),
        ("Table Creation", test_create_table),
        ("Insert & Query", test_insert_and_query),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = await test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n✓ All tests passed! Database is ready to use.")
    else:
        print("\n✗ Some tests failed. Please check the configuration.")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
