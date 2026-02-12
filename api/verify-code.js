export default async function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email, code } = req.body;

    if (!email || !code) {
        return res.status(400).json({ error: 'Email and code are required' });
    }

    // Get codes from global storage
    const codes = global.codes || new Map();
    const storedData = codes.get(email);

    if (!storedData) {
        return res.status(400).json({ success: false, error: 'Code not found' });
    }

    if (Date.now() > storedData.expires) {
        codes.delete(email);
        return res.status(400).json({ success: false, error: 'Code expired' });
    }

    if (storedData.code !== code) {
        return res.status(400).json({ success: false, error: 'Invalid code' });
    }

    // Code is valid, remove it
    codes.delete(email);

    console.log(`Code verified for ${email}`);
    return res.status(200).json({ success: true });
}
