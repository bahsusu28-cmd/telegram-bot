const { codes } = require('./send-code');

module.exports = async (req, res) => {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email, code } = req.body;

    if (!email || !code) {
        return res.status(400).json({ error: 'Email and code are required' });
    }

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

    res.status(200).json({ success: true });
};
