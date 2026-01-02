import { db } from '../lib/db/drizzle';
import { sql } from 'drizzle-orm';

async function main() {
    console.log('Pinging database...');
    try {
        // Execute a simple query to check connection
        const result = await db.execute(sql`SELECT 1`);
        console.log('✅ Database connection successful!');
        console.log('Result:', result);
    } catch (error) {
        console.error('❌ Database connection failed:', error);
    }
    process.exit(0);
}

main();
