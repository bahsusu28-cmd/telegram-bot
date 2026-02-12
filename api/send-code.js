const nodemailer = require('nodemailer');

// Store codes in memory (temporary solution)
global.codes = global.codes || new Map();

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

    const { email } = req.body;

    if (!email) {
        return res.status(400).json({ error: 'Email is required' });
    }

    // Generate 6-digit code
    const code = Math.floor(100000 + Math.random() * 900000).toString();

    // Store code with expiration (5 minutes)
    global.codes.set(email, {
        code: code,
        expires: Date.now() + 5 * 60 * 1000
    });

    try {
        // Create transporter
        const transporter = nodemailer.createTransport({
            host: 'mail.inbox.eu',
            port: 587,
            secure: false,
            auth: {
                user: 'verised@inbox.eu',
                pass: 'creator!!1340verised'
            },
            tls: {
                rejectUnauthorized: false
            }
        });

        // Send email
        await transporter.sendMail({
            from: '"Verised" <verised@inbox.eu>',
            to: email,
            subject: 'Код подтверждения Verised',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #ffc107;">⚡ Verised</h2>
                    <p style="font-size: 16px;">Ваш код подтверждения:</p>
                    <h1 style="color: #ffc107; font-size: 36px; letter-spacing: 5px; margin: 20px 0;">${code}</h1>
                    <p style="color: #666; font-size: 14px;">Код действителен 5 минут.</p>
                    <p style="color: #999; font-size: 12px; margin-top: 30px;">Если вы не запрашивали этот код, проигнорируйте это письмо.</p>
                </div>
            `
        });

        console.log(`Code sent to ${email}: ${code}`);
        return res.status(200).json({ success: true });
    } catch (error) {
        console.error('Email error:', error);
        return res.status(500).json({ 
            error: 'Failed to send email',
            details: error.message 
        });
    }
}
