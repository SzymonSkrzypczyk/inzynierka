import postgres from 'postgres';
import dotenv from 'dotenv';
import fs from 'fs';
dotenv.config({ path: '.env.local' });

const sql = postgres(process.env.DATABASE_URL!);

async function inspectTable(keywords: string[]) {
    const tables = await sql`
    SELECT tablename 
    FROM pg_catalog.pg_tables 
    WHERE schemaname = 'public'
  `;

    const match = tables.find(t => keywords.every(k => t.tablename.toLowerCase().includes(k.toLowerCase())));

    let output = '';
    if (match) {
        const tableName = match.tablename;
        output += `\nMatching Table for [${keywords.join(', ')}]: ${tableName}\n`;
        const columns = await sql`
      SELECT column_name, data_type 
      FROM information_schema.columns 
      WHERE table_name = ${tableName}
      ORDER BY ordinal_position
    `;
        for (const col of columns) {
            output += `  - ${col.column_name}: ${col.data_type}\n`;
        }
    } else {
        output += `\nNo table found for keywords: [${keywords.join(', ')}]\n`;
    }
    return output;
}

async function main() {
    let fullOutput = '';
    fullOutput += await inspectTable(['planetary', 'k']);
    fullOutput += await inspectTable(['dscovr', 'mag']);
    fullOutput += await inspectTable(['primary', 'integral', 'proton']);
    fullOutput += await inspectTable(['primary', 'xray']);
    fullOutput += await inspectTable(['solar', 'region']);

    fs.writeFileSync('db-schema-output.txt', fullOutput);
    console.log('Schema output written to db-schema-output.txt');
    process.exit(0);
}

main().catch(console.error);
