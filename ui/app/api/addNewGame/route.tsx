import { MongoClient } from 'mongodb';
export const dynamic = 'force-dynamic' // defaults to auto

const mongoURI = process.env.MONGODB_URI || "default_uri"

const client = new MongoClient(mongoURI)

export async function POST(request: Request) {
    await client.connect();
    const db = client.db(process.env.MONGODB_DB || 'default_db');
    const AGcollection = db.collection('active_game');

    const formData = await request.formData();
    const data: Record<string, string> = {};
    for (const [name, value] of formData.entries()) {
        data[name] = value.toString(); 
    }

    const documentsToInsert = [
        { id: 0, player_count: parseInt(data["players"]), max_score: parseInt(data["points"]) }
    ];

    await AGcollection.deleteMany({});
    AGcollection.insertMany(documentsToInsert)



    return new Response('Documents inserted successfully', { status: 200 });
}
