import { MongoClient } from 'mongodb';
export const dynamic = 'force-dynamic' // defaults to auto

const mongoURI = process.env.MONGODB_URI || "default_uri"

const client = new MongoClient(mongoURI)

export async function GET(request: Request) {
  await client.connect();
  const db = client.db(process.env.MONGODB_DB || 'default_db');
  const collection = db.collection('active_game');
  const data = await collection.find({}).toArray();
   
  await client.close();

  return Response.json({ data })
}
